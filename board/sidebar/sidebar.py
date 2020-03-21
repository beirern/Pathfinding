import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height, bg="grey")
        self.pack()

        # square_image = tk.PhotoImage(file="./static/square.png")
        # label = tk.Label(self, image=square_image)
        # label.image = square_image
        # label.grid(row=0)

        save_button = tk.Button(self, text="Save", fg="blue")
        save_button.grid(row=1)

        self.width = width
        self.height = height
