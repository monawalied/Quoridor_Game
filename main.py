# main.py
import tkinter as tk
from board_ui import BoardUI, ModeSelectScreen


def launch_menu(root):
    def on_start(mode, difficulty):
        BoardUI(root, mode=mode, difficulty=difficulty)
    ModeSelectScreen(root, on_start)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quoridor Strategy Engine")
    root.geometry("700x700")
    root.configure(bg="#1e2732")
    root.resizable(False, False)
    launch_menu(root)
    root.mainloop()