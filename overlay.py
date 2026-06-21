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
        self.bind("<MouseWheel>", func=self.on_scroll)
        self.bind("w", func=lambda ev: self.change_id(1))
        self.bind("s", func=lambda ev: self.change_id(-1))

        sty = ttk.Style()
        sty.configure("F1.TFrame", background="#DEDEDE")

        self.frame = ttk.Frame(self, style="F1.TFrame")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.bind("<Configure>", self.on_configure_frame)

        self.canvas = tk.Canvas(self.frame, background="#DEDEDE", highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_configure_canvas)
        self.canvas.create_text(0, 0, text=self.id_str, font=("Arial", 20, "bold"), fill="#FF0000")
        self.after_proc_id = None

        self.snip_size = 20

    def on_quit(self) -> None:
        if self.after_proc_id is not None:
            self.after_cancel(self.after_proc_id)
        self.destroy()

    def update_overlay(self) -> None:
        self.attributes("-topmost", True)
        self.canvas.delete("all")
        self.canvas.create_text(0, 0, text=self.id_str, font=("Arial", 20, "bold"), fill="#FF0000")

        self.after_proc_id = self.after(50, self.update_overlay)

    def on_configure_frame(self, event) -> None:
        self.frame.pack(fill=tk.BOTH, expand=True)

    def on_configure_canvas(self, event) -> None:
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.delete("all")
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, text=self.id_str, font=("Arial", self.snip_size, "bold"), fill="#FF0000")

    def on_scroll(self, event) -> None:
        sd = event.delta / 20
        self.snip_size = int(max(0, self.snip_size + sd))

    def change_id(self, d) -> None:
        self.building_id = max(0, self.building_id + d)
        self.id_str = f"{self.borough}_{self.building_id}"

    def run(self) -> None:
        self.update_overlay()
        self.focus_force()
        self.mainloop()