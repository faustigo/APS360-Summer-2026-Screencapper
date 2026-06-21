import tkinter as tk
from tkinter import ttk
import os

class Main(tk.Tk):

    def __init__(self):
        super(Main, self).__init__()
        self.frame = ttk.Frame(self, padding = 10)
        self.frame.grid()
        ttk.Label(self.frame, text = "Hello world!").grid(column = 0, row = 0)
        ttk.Button(self.frame, text = "Quit", command = self.on_quit).grid(column = 0, row = 1)
        self.bind("<Escape>", func = lambda ev: self.on_quit)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

    def on_quit(self):
        v = 0
        try:
            with open("out/number.txt", "r") as f:
                c = f.read()
                v = 0 if len(c) < 1 else int(c) + 1
        except IOError:
            pass
        if not os.path.exists("out/"):
            os.mkdir("out")
        with open("out/number.txt", "w") as f:
            f.write(str(v))
        self.destroy()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    Main().run()