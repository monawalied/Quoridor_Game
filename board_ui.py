# board_ui.py
import tkinter as tk
from tkinter import messagebox
from game_logic import GameLogic
from Ai_Agent import get_ai_move


# ---------------------------------------------------------------------------
# Mode Selection Screen
# ---------------------------------------------------------------------------

class ModeSelectScreen:
    def __init__(self, root, on_start):
        self.root     = root
        self.on_start = on_start
        self.mode       = tk.StringVar(value="hvh")
        self.difficulty = tk.StringVar(value="medium")
        self._build()

    def _build(self):
        self.frame = tk.Frame(self.root, bg="#1e2732")
        self.frame.pack(expand=True, fill="both")

        tk.Label(self.frame, text="QUORIDOR",
                 fg="#f1c40f", bg="#1e2732",
                 font=("Courier", 32, "bold")).pack(pady=(60, 5))

        tk.Label(self.frame, text="Strategy Board Game",
                 fg="#8a9aa7", bg="#1e2732",
                 font=("Courier", 11)).pack(pady=(0, 40))

        tk.Label(self.frame, text="Select Game Mode",
                 fg="#ecf0f1", bg="#1e2732",
                 font=("Arial", 13, "bold")).pack(pady=(0, 10))

        for text, val in [("👤  Human vs Human", "hvh"), ("🤖  Human vs Computer", "hvc")]:
            tk.Radiobutton(self.frame, text=text, variable=self.mode, value=val,
                           bg="#1e2732", fg="#ecf0f1", selectcolor="#2c3e50",
                           activebackground="#1e2732", activeforeground="#f1c40f",
                           font=("Arial", 12), command=self._toggle_difficulty).pack(anchor="center", pady=3)

        self.diff_frame = tk.Frame(self.frame, bg="#1e2732")
        self.diff_frame.pack(pady=(20, 5))

        tk.Label(self.diff_frame, text="AI Difficulty",
                 fg="#ecf0f1", bg="#1e2732",
                 font=("Arial", 11, "bold")).pack(pady=(0, 8))

        for label, val in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            tk.Radiobutton(self.diff_frame, text=label, variable=self.difficulty, value=val,
                           bg="#1e2732", fg="#ecf0f1", selectcolor="#2c3e50",
                           activebackground="#1e2732", activeforeground="#f1c40f",
                           font=("Arial", 11)).pack(side="left", padx=12)

        tk.Button(self.frame, text="Start Game", command=self._start,
                  bg="#f1c40f", fg="#1e2732", font=("Arial", 13, "bold"),
                  padx=30, pady=8, relief="flat",
                  activebackground="#d4ac0d", cursor="hand2").pack(pady=30)

        self._toggle_difficulty()

    def _toggle_difficulty(self):
        state = "normal" if self.mode.get() == "hvc" else "disabled"
        for w in self.diff_frame.winfo_children():
            try:
                w.config(state=state)
            except Exception:
                pass

    def _start(self):
        mode       = self.mode.get()
        difficulty = self.difficulty.get() if mode == "hvc" else None
        self.frame.destroy()
        self.on_start(mode, difficulty)


# ---------------------------------------------------------------------------
# Main Board UI
# ---------------------------------------------------------------------------

class BoardUI:
    def __init__(self, root, mode="hvh", difficulty=None):
        self.root       = root
        self.mode       = mode
        self.difficulty = difficulty
        self.logic      = GameLogic()

        self.cell_size        = 45
        self.wall_thickness   = 10
        self.wall_orientation = 'H'
        self.hover_wall       = None
        self.last_mouse_event = None

        self.root.configure(bg="#1e2732")
        board_width = (self.logic.board_size * self.cell_size +
                       (self.logic.board_size - 1) * self.wall_thickness)

        self.main_frame = tk.Frame(root, bg="#1e2732")
        self.main_frame.pack(pady=20, padx=20)

        self.canvas = tk.Canvas(self.main_frame, width=board_width, height=board_width,
                                bg="#111923", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=5)

        self.info_frame = tk.Frame(self.main_frame, bg="#1e2732")
        self.info_frame.grid(row=1, column=0, pady=5)

        self.turn_label = tk.Label(self.info_frame, text="Player 1's Turn (Red)",
                                   fg="#e74c3c", bg="#1e2732", font=("Arial", 12, "bold"))
        self.turn_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.p1_label = tk.Label(self.info_frame, text="Red Walls Left: 10",
                                 fg="#e74c3c", bg="#1e2732", font=("Arial", 10, "bold"), padx=20)
        self.p1_label.grid(row=1, column=0)

        self.p2_label = tk.Label(self.info_frame, text="Blue Walls Left: 10",
                                 fg="#3498db", bg="#1e2732", font=("Arial", 10, "bold"), padx=20)
        self.p2_label.grid(row=1, column=1)

        tk.Label(self.main_frame, text="Click [Space] to rotate wall",
                 fg="#8a9aa7", bg="#1e2732", font=("Arial", 9, "italic")).grid(row=2, column=0, pady=5)

        self.button_frame = tk.Frame(self.main_frame, bg="#1e2732")
        self.button_frame.grid(row=3, column=0, pady=10)

        tk.Button(self.button_frame, text="Reset Game", command=self.restart_game_ui,
                  bg="#e74c3c", fg="white", font=("Arial", 12, "bold"),
                  padx=15, pady=5, relief="flat",
                  activebackground="#c0392b", activeforeground="white").pack(side="left", padx=8)

        tk.Button(self.button_frame, text="Main Menu", command=self.go_to_menu,
                  bg="#2c3e50", fg="white", font=("Arial", 12, "bold"),
                  padx=15, pady=5, relief="flat",
                  activebackground="#1a252f", activeforeground="white").pack(side="left", padx=8)

        if self.mode == "hvc":
            diff_text = difficulty.capitalize() if difficulty else "Medium"
            tk.Label(self.main_frame,
                     text=f"Mode: Human vs AI  |  Difficulty: {diff_text}",
                     fg="#f1c40f", bg="#1e2732", font=("Arial", 9, "italic")).grid(row=4, column=0, pady=2)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>",   self.show_hover_wall)
        self.root.bind("<space>",      self.toggle_orientation)

        self.refresh_display()

    # ── Drawing ──────────────────────────────────────────────────────────────

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
                self.canvas.create_rectangle(x1, y1,
                                             x1 + self.cell_size, y1 + self.cell_size,
                                             fill="#2c3e50", outline="#34495e", width=1)

    def draw_pawns(self):
        padding = 6
        r1, c1 = self.logic.player1_pos
        x1 = c1 * (self.cell_size + self.wall_thickness)
        y1 = r1 * (self.cell_size + self.wall_thickness)
        self.canvas.create_oval(x1+padding, y1+padding,
                                x1+self.cell_size-padding, y1+self.cell_size-padding,
                                fill="#e74c3c", outline="#ffffff", width=2)

        r2, c2 = self.logic.player2_pos
        x2 = c2 * (self.cell_size + self.wall_thickness)
        y2 = r2 * (self.cell_size + self.wall_thickness)
        self.canvas.create_oval(x2+padding, y2+padding,
                                x2+self.cell_size-padding, y2+self.cell_size-padding,
                                fill="#3498db", outline="#ffffff", width=2)

    def draw_walls(self):
        for (r, c) in self.logic.walls_h:
            x1 = c * (self.cell_size + self.wall_thickness)
            y1 = (r+1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            self.canvas.create_rectangle(x1, y1,
                                         x1 + 2*self.cell_size + self.wall_thickness,
                                         y1 + self.wall_thickness,
                                         fill="#f1c40f", outline="")

        for (r, c) in self.logic.walls_v:
            x1 = (c+1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            y1 = r * (self.cell_size + self.wall_thickness)
            self.canvas.create_rectangle(x1, y1,
                                         x1 + self.wall_thickness,
                                         y1 + 2*self.cell_size + self.wall_thickness,
                                         fill="#f1c40f", outline="")

    def draw_hover_preview(self):
        if not self.hover_wall or self.logic.game_over:
            return
        if self.mode == "hvc" and self.logic.current_player == 2:
            return
        (r, c), orient = self.hover_wall
        valid = (self.logic.check_geometric_validity(r, c, orient) and
                 self.logic.is_wall_placement_valid(r, c, orient))
        color = "#2ecc71" if valid else "#e74c3c"
        if orient == 'H':
            x1 = c * (self.cell_size + self.wall_thickness)
            y1 = (r+1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            x2 = x1 + 2*self.cell_size + self.wall_thickness
            y2 = y1 + self.wall_thickness
        else:
            x1 = (c+1) * (self.cell_size + self.wall_thickness) - self.wall_thickness
            y1 = r * (self.cell_size + self.wall_thickness)
            x2 = x1 + self.wall_thickness
            y2 = y1 + 2*self.cell_size + self.wall_thickness
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, stipple="gray50", outline="")

    def show_hover_wall(self, event):
        if self.logic.game_over:
            return
        if self.mode == "hvc" and self.logic.current_player == 2:
            return
        self.last_mouse_event = event
        slot = self.cell_size + self.wall_thickness
        col, row = event.x // slot, event.y // slot
        ox,  oy  = event.x % slot,  event.y % slot
        if ((ox >= self.cell_size - 6 or oy >= self.cell_size - 6) and
                0 <= row < self.logic.board_size - 1 and
                0 <= col < self.logic.board_size - 1):
            self.hover_wall = ((row, col), self.wall_orientation)
        else:
            self.hover_wall = None
        self.refresh_display()

    # ── Click handler ────────────────────────────────────────────────────────

    def on_canvas_click(self, event):
        if self.logic.game_over:
            return
        if self.mode == "hvc" and self.logic.current_player == 2:
            return

        # Wall placement
        if self.hover_wall:
            (r, c), orient = self.hover_wall
            if self.logic.is_wall_placement_valid(r, c, orient):
                self.logic.place_wall(r, c, orient)
                self.hover_wall = None
                self.check_match_status()
                self._maybe_trigger_ai()
                return

        # Pawn movement
        slot = self.cell_size + self.wall_thickness
        col, row = event.x // slot, event.y // slot
        ox,  oy  = event.x % slot,  event.y % slot

        if ox < self.cell_size and oy < self.cell_size:
            active_pos = self.logic.player1_pos if self.logic.current_player == 1 else self.logic.player2_pos
            opp_pos    = self.logic.player2_pos if self.logic.current_player == 1 else self.logic.player1_pos

            if (row, col) in self.logic.get_valid_moves(active_pos, opp_pos):
                self.logic.move_pawn(row, col)
                self.check_match_status()
                self._maybe_trigger_ai()

    # ── AI ───────────────────────────────────────────────────────────────────

    def _maybe_trigger_ai(self):
        if self.mode != "hvc" or self.logic.game_over:
            return
        if self.logic.current_player == 2:
            self.root.after(400, self._run_ai_turn)

    def _run_ai_turn(self):
        if self.logic.game_over:
            return

        action = get_ai_move(self.logic, self.difficulty or "medium")

        if action is None:
            return

        action_type, action_data = action

        if action_type == "move":
            r, c = action_data
            self.logic.move_pawn(r, c)
        else:
            r, c, orient = action_data
            self.logic.place_wall(r, c, orient)

        self.check_match_status()

    # ── Status & controls ────────────────────────────────────────────────────

    def check_match_status(self):
        self.refresh_display()
        winner = self.logic.check_win_condition()
        if winner > 0:
            self.logic.game_over = True
            if self.mode == "hvc":
                msg = "You win! 🎉" if winner == 1 else "The AI wins!"
            else:
                msg = f"Player {winner} has won!"
            messagebox.showinfo("Game Over", msg)

    def update_ui_labels(self):
        p1_name = "You (Red)"    if self.mode == "hvc" else "Player 1 (Red)"
        p2_name = "AI (Blue)"   if self.mode == "hvc" else "Player 2 (Blue)"

        if self.logic.current_player == 1:
            self.turn_label.config(text=f"{p1_name}'s Turn", fg="#e74c3c")
        else:
            self.turn_label.config(text=f"{p2_name}'s Turn", fg="#3498db")

        self.p1_label.config(text=f"Red Walls Left: {self.logic.player1_walls_left}")
        self.p2_label.config(text=f"Blue Walls Left: {self.logic.player2_walls_left}")

    def restart_game_ui(self):
        self.logic.reset_state()
        self.hover_wall       = None
        self.wall_orientation = 'H'
        self.refresh_display()

    def go_to_menu(self):
        self.main_frame.destroy()
        self.root.unbind("<space>")
        from main import launch_menu
        launch_menu(self.root)