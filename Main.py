import tkinter as tk
from tkinter import ttk
import os
import typing

OPTIONS = ("-", "OldToronto", "York", "EastYork", "NorthYork", "Etobicoke", "Scarborough")

class Main(tk.Tk):

    def __init__(self):
        """ Initialize the options window. """
        super(Main, self).__init__()
        self.title("APS360 Screencapper")
        self.geometry("300x150+0+0")
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.bind("<Escape>", func=lambda ev: self.on_quit())

        self.current_borough = tk.StringVar()
        self.current_borough.set(OPTIONS[0])

        self.building_id = tk.IntVar()
        self.building_id.set(0)

        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()

        ttk.Label(self.frame, text="Borough").grid(column=0, row=0, sticky="w", pady=5)

        self.borough_om = ttk.OptionMenu(self.frame, self.current_borough, *OPTIONS, direction="below")
        self.borough_om.config(width=12)
        self.borough_om.grid(column=1, row=0, sticky="w")

        ttk.Label(self.frame, text="Building ID").grid(column=0, row=1, sticky="w", padx=(0, 20), pady=5)

        self.building_entry = ttk.Entry(self.frame, width=4)
        self.building_entry.insert(0, str(self.building_id.get()))
        self.building_entry.grid(column=1, row=1, sticky="w")

    def on_quit(self) -> None:
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

    def run(self) -> None:
        self.mainloop()

    def get_current_picture_id_components(self) -> typing.Union[None, tuple[str, str]]:
        """ Returns (borough, building_id) if the borough is set and the building id is a valid integer; otherwise, return None."""
        v = self.current_borough.get()
        if v == OPTIONS[0] or v not in OPTIONS:
            return None
        return v, f"{self.building_id.get()}"

if __name__ == "__main__":
    Main().run()