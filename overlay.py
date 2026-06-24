import tkinter as tk
import tkinter.ttk as ttk
import os
import mss
import cv2
import numpy
import numpy as np
import itertools

class Overlay(tk.Tk):

    def __init__(self, borough: str, building_id: int):
        super(Overlay, self).__init__()
        self.borough = borough
        self.building_id = building_id
        self.id_str = f"{self.borough}_{self.building_id}"

        key = "#000000"
        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.5)
        self.config(background=key)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.bind("<Escape>", func=lambda ev: self.on_quit())
        self.bind("<MouseWheel>", func=self.on_scroll)
        self.bind("<Motion>", func=self.on_motion)
        self.bind("<ButtonRelease-1>", func=self.take_screenshot)
        self.bind("w", func=lambda ev: self.change_id(1))
        self.bind("s", func=lambda ev: self.change_id(-1))

        sty = ttk.Style()
        sty.configure("F1.TFrame", background=key)

        self.frame = ttk.Frame(self, style="F1.TFrame")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.bind("<Configure>", self.on_configure_frame)

        self.canvas = tk.Canvas(self.frame, background=key, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_configure_canvas)
        self.after_proc_id = None

        self.snip_size = 500
        self.screenshot_x = 0
        self.screenshot_y = 0

    def on_quit(self) -> None:
        if self.after_proc_id is not None:
            self.after_cancel(self.after_proc_id)
        self.destroy()

    def update_overlay(self) -> None:
        self.attributes("-topmost", True)
        self.update_canvas()
        if self.after_proc_id is not None: # Don't double-call this function
            self.after_cancel(self.after_proc_id)
        self.after_proc_id = self.after(50, self.update_overlay)

    def update_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.screenshot_x, self.screenshot_y, text=self.id_str, font=("Arial", 15, "bold"), fill="#FF0000", anchor=tk.NW)
        self.canvas.create_rectangle(self.screenshot_x, self.screenshot_y, self.screenshot_x + self.snip_size, self.screenshot_y + self.snip_size, outline="red", width=1, fill="")

    def on_configure_frame(self, event) -> None:
        self.frame.pack(fill=tk.BOTH, expand=True)

    def on_configure_canvas(self, event) -> None:
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.update_canvas()

    def on_scroll(self, event) -> None:
        sd = event.delta / 20
        self.snip_size = int(max(0, self.snip_size + sd))

    def change_id(self, d) -> None:
        self.building_id = max(0, self.building_id + d)
        self.id_str = f"{self.borough}_{self.building_id}"

    def on_motion(self, event):
        self.screenshot_x, self.screenshot_y = event.x, event.y

    def take_screenshot(self, event):
        """ Create screenshot and resize it. """
        self.withdraw() # Hide window
        if not os.path.exists("out/"):
            os.mkdir("out")
        if not os.path.exists(f"out/{self.borough}/"):
            os.mkdir(f"out/{self.borough}")

        TARGET_SIZE = (500, 500)
        with mss.MSS() as sct:
            # TODO select window and ignore overlay
            monitor = { "top": self.screenshot_y, "left": self.screenshot_x, "width": self.snip_size, "height": self.snip_size }
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            scaled = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_AREA)

            # find appropriate filename
            c = itertools.count(start=1)
            file_id = f"out/{self.borough}/{self.id_str}_{next(c)}.jpg"
            while os.path.exists(file_id):
                file_id = f"out/{self.borough}/{self.id_str}_{next(c)}.jpg"
            cv2.imwrite(file_id, scaled)

        self.deiconify() # Reshow window

    def run(self) -> None:
        self.update_overlay()
        self.focus_force()
        self.mainloop()