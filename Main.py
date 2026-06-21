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
        self.geometry("400x150+0+0")
        self.minsize(400, 150)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.bind("<Escape>", func=lambda ev: self.on_quit())
        self.bind("<Up>", func=lambda ev: self.increment_building_id())
        self.bind("<Down>", func=lambda ev: self.decrement_building_id())

        self.current_borough = tk.StringVar()
        self.current_borough.set(OPTIONS[0])

        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()

        ttk.Label(self.frame, text="Borough").grid(column=0, row=0, sticky="w", pady=5)

        self.borough_om = ttk.OptionMenu(self.frame, self.current_borough, *OPTIONS, direction="below")
        self.borough_om.config(width=12)
        self.borough_om.grid(column=1, row=0, sticky="w")

        self.error_borough_lbl = ttk.Label(self.frame, text="Select a borough.", foreground="#FF0000")
        self.error_borough_lbl.grid_forget()

        ttk.Label(self.frame, text="Building ID").grid(column=0, row=1, sticky="w", padx=(0, 20), pady=5)

        self.building_entry = ttk.Entry(self.frame, width=6)
        self.building_entry.insert(0, "0")
        self.building_entry.grid(column=1, row=1, sticky="w")

        self.error_id_lbl = ttk.Label(self.frame, text="Must be a valid ID >= 0.", foreground="#FF0000")
        self.error_id_lbl.grid_forget()

        ttk.Button(self.frame, text="Go", width=12, command=lambda: self.get_current_picture_id_components()).grid(column=0, row=2, sticky="w", pady=5)

    def on_quit(self) -> None:
        self.destroy()

    def run(self) -> None:
        self.mainloop()

    def get_current_picture_id_components(self) -> typing.Union[None, tuple[str, str]]:
        """ Returns (borough, building_id) if the borough is set and the building id is a valid integer; otherwise, return None."""
        valid = True

        borough = self.current_borough.get()
        if borough == OPTIONS[0] or borough not in OPTIONS:
            self.error_borough_lbl.grid(column=2, row=0, sticky="w", padx=(10, 0))
            valid = False
        else:
            self.error_borough_lbl.grid_forget()

        building_id = self.building_entry.get()
        if not building_id.isdigit() or int(building_id) < 0:
            self.error_id_lbl.grid(column=2, row=1, sticky="w", padx=(10, 0))
            valid = False
        else:
            self.error_id_lbl.grid_forget()

        return (borough, f"{building_id}") if valid else None

    def increment_building_id(self) -> None:
        building_id = self.building_entry.get()
        self.building_entry.delete(0, tk.END)
        self.building_entry.insert(0, str(max(0, int(building_id) + 1)) if building_id.isdigit() else "0")

    def decrement_building_id(self) -> None:
        building_id = self.building_entry.get()
        self.building_entry.delete(0, tk.END)
        self.building_entry.insert(0, str(max(0, int(building_id) - 1)) if building_id.isdigit() else "0")

if __name__ == "__main__":
    Main().run()