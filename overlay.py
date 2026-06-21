import tkinter as tk
import tkinter.ttk as ttk
import os

class Overlay(tk.Tk):

    def __init__(self, borough: str, building_id: int):
        super(Overlay, self).__init__()
        self.borough = borough
        self.building_id = building_id
        self.id_str = f"{self.borough}_{self.building_id}"

        self.attributes("-fullscreen", True)
        self.attributes("-transparentcolor", "#DEDEDE")
        self.config(background="#DEDEDE")

        self.bind("<Escape>", func=lambda ev: self.on_quit())

        sty = ttk.Style()
        sty.configure("F1.TFrame", background="#CCCCCC")

        self.frame = ttk.Frame(self, style="F1.TFrame")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.bind("<Configure>", self.on_configure_frame)

        self.canvas = tk.Canvas(self.frame, background="#DEDEDE", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_configure_canvas)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, text=self.id_str, font=("Arial", 20, "bold"), fill="#FF0000")
        self.after_proc_id = None

    def on_quit(self) -> None:
        if self.after_proc_id is not None:
            self.after_cancel(self.after_proc_id)
        self.destroy()

    def update_overlay(self) -> None:
        self.attributes("-topmost", True)
        self.after_proc_id = self.after(50, self.update_overlay)

    def on_configure_frame(self, event) -> None:
        self.frame.pack(fill=tk.BOTH, expand=True)

    def on_configure_canvas(self, event) -> None:
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.delete("all")
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, text=self.id_str, font=("Arial", 20, "bold"), fill="#FF0000")

    def run(self) -> None:
        self.update_overlay()
        self.focus_force()
        self.mainloop()