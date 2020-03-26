import tkinter as tk


class Sidebar(tk.Frame):
    def __init__(self, master=None, width=0, height=0):
        super().__init__(master=master, width=width, height=height)
        self.pack()

        # Radio Buttons
        self.v = tk.IntVar()
        self.v.set(1)

        self.wall = tk.Radiobutton(
            self, text='Walls', variable=self.v, value=1)
        self.wall.grid(row=0)
        self.waypoint = tk.Radiobutton(
            self, text='Waypoints', variable=self.v, value=2)
        self.waypoint.grid(row=1)

        # Save Button
        self.save_button = tk.Button(self, text='Save', fg='blue')
        self.save_button.grid(row=2)

        # Load Button
        self.load_button = tk.Button(self, text='Load', fg='blue')
        self.load_button.grid(row=3)

        # Editable Option
        self.v1 = tk.IntVar()
        self.v1.set(1)
        self.editable = tk.Checkbutton(self, text='Editable', variable=self.v1)
        self.editable.grid(row=4)

        self.width = width
        self.height = height
