import tkinter as tk
from tkinter import messagebox

class QuoridorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quoridor Game")
        self.root.configure(bg="#1e2732")  
        self.board_size = 9   
        self.cell_size = 45       
        self.wall_thickness = 8   
        
        board_width = (self.board_size * self.cell_size) + ((self.board_size - 1) * self.wall_thickness)
        self.canvas = tk.Canvas(root, width=board_width, height=board_width, bg="#111923", highlightthickness=0)
        self.canvas.pack(pady=20, padx=20)  

        #two players first position
        self.player1_pos = (8, 4)
        self.player2_pos = (0, 4)

        self.current_player = 1
        self.game_over = False

        self.button_frame = tk.Frame(root, bg="#1e2732")
        self.button_frame.pack(pady=10)
        
        self.restart_btn = tk.Button(
            self.button_frame, 
            text="Restart Game", 
            command=self.restart_game, 
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
        self.restart_game()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.draw_board_cells()
        self.draw_pawns()

    # board 
    def draw_board_cells(self):
        self.canvas.delete('all') 
        for r in range(self.board_size):
            for c in range(self.board_size): 
                x1 = c * (self.cell_size + self.wall_thickness)
                y1 = r * (self.cell_size + self.wall_thickness)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size     

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill="#2c3e50",      
                    outline="#34495e",    
                    width=1            
                )

    #pawns            
    def draw_pawns(self):
        self.canvas.delete('pawn')     
        r1, c1 = self.player1_pos
        x1 = c1 * (self.cell_size + self.wall_thickness)
        y1 = r1 * (self.cell_size + self.wall_thickness)
        
        padding = 6
        self.canvas.create_oval(
            x1 + padding, y1 + padding, 
            x1 + self.cell_size - padding, y1 + self.cell_size - padding,
            fill="#e74c3c",   
            outline="#ffffff", 
            width=2,
            tags='pawn'     
        )
        
        r2, c2 = self.player2_pos
        x2 = c2 * (self.cell_size + self.wall_thickness)
        y2 = r2 * (self.cell_size + self.wall_thickness)
        
        self.canvas.create_oval(
            x2 + padding, y2 + padding, 
            x2 + self.cell_size - padding, y2 + self.cell_size - padding,
            fill="#3498db",    
            outline="#ffffff",
            width=2,
            tags='pawn'
        )

    # Restart button
    def restart_game(self):
        self.player1_pos = (8, 4)
        self.player2_pos = (0, 4)
        self.current_player = 1
        self.game_over = False
        self.draw_board_cells()
        self.draw_pawns()
        print("Game restarted! Player 1's turn.")    

    def get_valid_moves(self, current_pos):
        r, c = current_pos
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.current_player == 1:
            opponent_pos = self.player2_pos
        else:
            opponent_pos = self.player1_pos
        
        for dr, dc in directions:
            next_r = r + dr
            next_c = c + dc
            
            if 0 <= next_r < self.board_size and 0 <= next_c < self.board_size:      
                if (next_r, next_c) == opponent_pos:
                    jump_r = next_r + dr
                    jump_c = next_c + dc

                    if 0 <= jump_r < self.board_size and 0 <= jump_c < self.board_size:
                        valid_moves.append((jump_r, jump_c))
                else:
                    valid_moves.append((next_r, next_c))
                
        return valid_moves
    
    def on_canvas_click(self, event):
        if self.game_over:
            return
        if self.player1_pos[0] == 0:
            self.game_over = True
            messagebox.showinfo("Game Over", "Player 1 (Red) Wins the Game!")

        elif self.player2_pos[0] == self.board_size - 1:
            self.game_over = True
            messagebox.showinfo("Game Over", "Player 2 (Blue) Wins the Game!")

    def on_canvas_click(self, event):
        slot_size = self.cell_size + self.wall_thickness
        clicked_col = event.x // slot_size
        clicked_row = event.y // slot_size
        
        if self.current_player == 1:
            active_pos = self.player1_pos
        else:
            active_pos = self.player2_pos

        allowed_moves = self.get_valid_moves(active_pos)

        if (clicked_row, clicked_col) in allowed_moves:
            if self.current_player == 1:
                self.player1_pos = (clicked_row, clicked_col)
                print(f"Player 1 (Red) moved to: Row {clicked_row}, Col {clicked_col}")

                if self.player1_pos[0] == 0:
                    self.game_over = True
                    self.draw_pawns() 
                    messagebox.showinfo("Game Over", "Player 1 (Red) Wins the Game!")
                    return              
                self.current_player = 2

            else:
                self.player2_pos = (clicked_row, clicked_col)
                print(f"Player 2 (Blue) moved to: Row {clicked_row}, Col {clicked_col}")
                if self.player2_pos[0] == self.board_size - 1:
                    self.game_over = True
                    self.draw_pawns()
                    messagebox.showinfo("Game Over", "Player 2 (Blue) Wins the Game!")
                    return
                self.current_player = 1
            self.draw_pawns()
        else:
            print(f"Invalid move ")

            
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoridorGame(root)
    root.mainloop()