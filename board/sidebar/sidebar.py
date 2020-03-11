import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height, bg="grey")
        self.pack()
