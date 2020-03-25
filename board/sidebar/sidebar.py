import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        # Radio Buttons
        self.v = tk.IntVar()
        self.v.set(1)

        self.wall = tk.Radiobutton(
            self, text="Walls", variable=self.v, value=1)
        self.wall.grid(row=0)
        self.waypoint = tk.Radiobutton(
            self, text="Waypoints", variable=self.v, value=2)
        self.waypoint.grid(row=1)

        # Save Button
        self.save_button = tk.Button(self, text="Save", fg="blue")
        self.save_button.grid(row=2)

        self.width = width
        self.height = height
