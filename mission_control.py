import tkinter as tk
import board

root = tk.Tk()
root.resizable(False, False)

board = board.Board(master=root, height=600, width=1200)

root.mainloop()
