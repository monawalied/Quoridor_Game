import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic

class BoardUI:
    def __init__(self, root):
        self.root = root
        self.logic = GameLogic()
        
        self.cell_size = 45       
        self.wall_thickness = 10   
        self.wall_orientation = 'H'
        self.hover_wall = None
        self.last_mouse_event = None

        self.root.configure(bg="#1e2732")
        board_width = (self.logic.board_size * self.cell_size) + ((self.logic.board_size - 1) * self.wall_thickness)

        # Central Layout Frame Container
        self.main_frame = tk.Frame(root, bg="#1e2732")
        self.main_frame.pack(pady=20, padx=20)

        # 9x9 Board Canvas [cite: 9, 31]
        self.canvas = tk.Canvas(self.main_frame, width=board_width, height=board_width, bg="#111923", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=5)

        # UI Info labels for Wall Count and Turns [cite: 41, 42]
        self.info_frame = tk.Frame(self.main_frame, bg="#1e2732")
        self.info_frame.grid(row=1, column=0, pady=5)
        
        self.turn_label = tk.Label(self.info_frame, text="Player 1's Turn (Red)", fg="#e74c3c", bg="#1e2732", font=("Arial", 12, "bold"))
        self.turn_label.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.p1_label = tk.Label(self.info_frame, text="Red Walls Left: 10", fg="#e74c3c", bg="#1e2732", font=("Arial", 10, "bold"), padx=20)
        self.p1_label.grid(row=1, column=0)
        
        self.p2_label = tk.Label(self.info_frame, text="Blue Walls Left: 10", fg="#3498db", bg="#1e2732", font=("Arial", 10, "bold"), padx=20)
        self.p2_label.grid(row=1, column=1)

        # Help Instruction Tooltip
        self.help_label = tk.Label(self.main_frame, text="Click [Space] to rotate wall", fg="#8a9aa7", bg="#1e2732", font=("Arial", 9, "italic"))
        self.help_label.grid(row=2, column=0, pady=5)

        # Button Frame Panel
        self.button_frame = tk.Frame(self.main_frame, bg="#1e2732")
        self.button_frame.grid(row=3, column=0, pady=10)
        
        self.restart_btn = tk.Button(
            self.button_frame, 
            text="Reset Game", 
            command=self.restart_game_ui, 
            bg="#e74c3c", 
            fg="white", 
            font=("Arial", 12, "bold"),
            padx=15, 
            pady=5,
            relief="flat",
            activebackground="#c0392b",
            activeforeground="white"
        )
        self.restart_btn.pack()

        # Bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.show_hover_wall)
        self.root.bind("<space>", self.toggle_orientation)

        self.refresh_display()

    def toggle_orientation(self, event):
        self.wall_orientation = 'V' if self.wall_orientation == 'H' else 'H'
        if self.last_mouse_event:
            self.show_hover_wall(self.last_mouse_event)

    def refresh_display(self):
        self.canvas.delete('all')
        self.draw_board_cells()
        self.draw_walls()
        self.draw_hover_preview()
        self.draw_pawns()
        self.update_ui_labels()

    def draw_board_cells(self):
        for r in range(self.logic.board_size):
            for c in range(self.logic.board_size):
                x1 = c * (self.cell_size + self.wall_thickness)
                y1 = r * (self.cell_size + self.wall_thickness)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2c3e50", outline="#34495e", width=1)

    def draw_pawns(self):
        # Draw Player 1 (Red) [cite: 11]
        r1, c1 = self.logic.player1_pos
        x1 = c1 * (self.cell_size + self.wall_thickness)
        y1 = r1 * (self.cell_size + self.wall_thickness)
        padding = 6
        self.canvas.create_oval(
            x1 + padding, y1 + padding, 
            x1 + self.cell_size - padding, y1 + self.cell_size - padding,
            fill="#e74c3c",   
            outline="#ffffff", 
            width=2
        )
        
        # Draw Player 2 (Blue) [cite: 11]
        r2, c2 = self.logic.player2_pos
        x2 = c2 * (self.cell_size + self.wall_thickness)
        y2 = r2 * (self.cell_size + self.wall_thickness)
        self.canvas.create_oval(
            x2 + padding, y2 + padding, 
            x2 + self.cell_size - padding, y2 + self.cell_size - padding,
            fill="#3498db",    
            outline="#ffffff",
            width=2
        )

    def draw_walls(self):
        # Draw Locked Horizontal Walls (2 squares long) [cite: 21]
        for (r, c) in self.logic.walls_h:
            x1 = c * (self.cell_size + self.wall_thickness)
            y1 = (r + 1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            x2 = x1 + (2 * self.cell_size) + self.wall_thickness
            y2 = y1 + self.wall_thickness
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f1c40f", outline="")

        # Draw Locked Vertical Walls (2 squares long) [cite: 21]
        for (r, c) in self.logic.walls_v:
            x1 = (c + 1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            y1 = r * (self.cell_size + self.wall_thickness)
            x2 = x1 + self.wall_thickness
            y2 = y1 + (2 * self.cell_size) + self.wall_thickness
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f1c40f", outline="")

    def draw_hover_preview(self):
        if not self.hover_wall or self.logic.game_over: 
            return
        (r, c), orient = self.hover_wall
        
        valid = self.logic.check_geometric_validity(r, c, orient) and self.logic.is_wall_placement_valid(r, c, orient)
        preview_color = "#2ecc71" if valid else "#e74c3c"
        
        if orient == 'H':
            x1 = c * (self.cell_size + self.wall_thickness)
            y1 = (r + 1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            x2 = x1 + (2 * self.cell_size) + self.wall_thickness
            y2 = y1 + self.wall_thickness
        else:
            x1 = (c + 1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            y1 = r * (self.cell_size + self.wall_thickness)
            x2 = x1 + self.wall_thickness
            y2 = y1 + (2 * self.cell_size) + self.wall_thickness

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=preview_color, stipple="gray50", outline="")

    def show_hover_wall(self, event):
        if self.logic.game_over: 
            return
        self.last_mouse_event = event
        slot = self.cell_size + self.wall_thickness
        col, row = event.x // slot, event.y // slot
        ox, oy = event.x % slot, event.y % slot

        if (ox >= self.cell_size - 6 or oy >= self.cell_size - 6) and (0 <= row < self.logic.board_size - 1) and (0 <= col < self.logic.board_size - 1):
            self.hover_wall = ((row, col), self.wall_orientation)
        else:
            self.hover_wall = None
        self.refresh_display()

    def on_canvas_click(self, event):
        if self.logic.game_over: 
            return
        
        if self.hover_wall:
            (r, c), orient = self.hover_wall
            if self.logic.is_wall_placement_valid(r, c, orient):
                self.logic.place_wall(r, c, orient)
                self.hover_wall = None
                self.check_match_status()
                return

        slot = self.cell_size + self.wall_thickness
        col, row = event.x // slot, event.y // slot
        ox, oy = event.x % slot, event.y % slot

        if ox < self.cell_size and oy < self.cell_size:
            active_pos = self.logic.player1_pos if self.logic.current_player == 1 else self.logic.player2_pos
            opp_pos = self.logic.player2_pos if self.logic.current_player == 1 else self.logic.player1_pos
            
            if (row, col) in self.logic.get_valid_moves(active_pos, opp_pos):
                self.logic.move_pawn(row, col)
                self.check_match_status()

    def check_match_status(self):
        self.refresh_display()
        winner = self.logic.check_win_condition()
        if winner > 0:
            self.logic.game_over = True
            messagebox.showinfo("Match Finished", f"Player {winner} has claimed victory!")

    def update_ui_labels(self):
        if self.logic.current_player == 1:
            self.turn_label.config(text="Player 1's Turn (Red)", fg="#e74c3c")
        else:
            self.turn_label.config(text="Player 2's Turn (Blue)", fg="#3498db")
        self.p1_label.config(text=f"Red Walls Left: {self.logic.player1_walls_left}")
        self.p2_label.config(text=f"Blue Walls Left: {self.logic.player2_walls_left}")

    def restart_game_ui(self):
        self.logic.reset_state()
        self.hover_wall = None
        self.wall_orientation = 'H'
        self.refresh_display()