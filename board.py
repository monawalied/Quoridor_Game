import tkinter as tk

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

        #two players position
        self.player1_pos = (8, 4)
        self.player2_pos = (0, 4)

        self.current_player = 1
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.draw_board_cells()
        self.draw_pawns()

    # board 
    def draw_board_cells(self):
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
    # pawns
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
        
    def get_valid_moves(self, current_pos):
        r, c = current_pos
        valid_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            next_r = r + dr
            next_c = c + dc
            if 0 <= next_r < self.board_size and 0 <= next_c < self.board_size:
                valid_moves.append((next_r, next_c))
                
        return valid_moves    

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
                self.current_player = 2
            else:
                self.player2_pos = (clicked_row, clicked_col)
                print(f"Player 2 (Blue) moved to: Row {clicked_row}, Col {clicked_col}")
                self.current_player = 1
            self.draw_pawns()
        else:
            print(f"Invalid move ")

            
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoridorGame(root)
    root.mainloop()