# main.py
import tkinter as tk
from board_ui import BoardUI

class QuoridorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quoridor Strategy Engine")
        
        self.root.geometry("700x680") 
        self.root.configure(bg="#1e2732")
        
        self.board_screen = BoardUI(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoridorApp(root)
    root.mainloop()