import tkinter as tk
from PIL import Image, ImageTk
import mss
import numpy as np
import os
import json
import time

CONFIG_PATH = "config.json"

class TkSelector:
    def __init__(self, mode, log_func):
        self.mode = mode
        self.log_func = log_func
        self.root = tk.Toplevel()
        self.root.title("SØREN Selector")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross")
        
        # Capture screen with MSS and convert to PIL
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                sct_img = sct.grab(monitor)
                self.img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        except Exception as e:
            self.log_func(f"❌ Screen capture error: {e}")
            self.root.destroy()
            return
        
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.canvas = tk.Canvas(self.root, cursor="cross", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        
        self.rects = []
        self.current_rect = None
        self.start_x = None
        self.start_y = None
        
        # Number of rectangles based on mode
        if mode == "hud":
            h_size = 5
            try:
                if os.path.exists(CONFIG_PATH):
                    with open(CONFIG_PATH, 'r') as f: h_size = json.load(f).get("horde_size", 5)
            except: pass
            self.max_rects = int(h_size)
        elif mode == "pp_slots": self.max_rects = 4
        elif mode in ["combat", "single_slot", "hp_bar", "status_slot", "sleep_icon", "battle_msg", "hunter_hp"]: self.max_rects = 1
        else: self.max_rects = 2
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.log_func(f"💡 [{mode.upper()} MODE] Draw {self.max_rects} rectangle(s) with your mouse.")

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline="red", width=2)

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.current_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        x1, x2 = min(self.start_x, end_x), max(self.start_x, end_x)
        y1, y2 = min(self.start_y, end_y), max(self.start_y, end_y)
        self.rects.append((x1, y1, x2, y2))
        self.canvas.itemconfig(self.current_rect, outline="green")
        
        if len(self.rects) >= self.max_rects:
            self.root.after(500, self.save_and_exit)

    def save_and_exit(self):
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, 'r') as f: config = json.load(f)
            else: config = {}

            if self.mode == "hud":
                h_size = len(self.rects)
                slot_key = f"slots_{h_size}"
                config[slot_key] = {} 
                for i, r in enumerate(self.rects):
                    config[slot_key][f"slot_{i+1}"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                # También guardamos en 'slots' por compatibilidad básica
                config["slots"] = config[slot_key]
                self.log_func(f"✅ SUCCESS: {h_size} slots saved in {slot_key}.")
                
            elif self.mode == "single_slot":
                r = self.rects[0]
                config["slot_single"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: Single Slot zone saved.")

            elif self.mode == "combat":
                r = self.rects[0]
                config["button_run"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: 'Run' button zone saved.")

            elif self.mode == "hp_bar":
                r = self.rects[0]
                config["hp_bar_region"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: HP Bar region saved.")

            elif self.mode == "status_slot":
                r = self.rects[0]
                config["status_slot_region"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: Status slot region saved.")

            elif self.mode == "sleep_icon":
                asset_dir = "assets"
                if not os.path.exists(asset_dir): os.makedirs(asset_dir)
                r = self.rects[0]
                icon = self.img.crop((r[0], r[1], r[2], r[3]))
                icon.save(os.path.join(asset_dir, "status_sleep.png"))
                self.log_func(f"✅ SUCCESS: Sleep icon asset saved.")

            elif self.mode == "pp_slots":
                config["pp_slots"] = {}
                for i, r in enumerate(self.rects):
                    config["pp_slots"][f"slot_{i+1}"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: 4 PP slots calibrated.")

            elif self.mode == "battle_msg":
                r = self.rects[0]
                config["battle_msg_region"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: Battle message region saved.")

            elif self.mode == "hunter_hp":
                r = self.rects[0]
                config["hunter_hp_region"] = {"x1": r[0], "y1": r[1], "x2": r[2], "y2": r[3]}
                self.log_func(f"✅ SUCCESS: Hunter HP region saved.")

            elif self.mode == "assets":
                asset_dir = "assets"
                if not os.path.exists(asset_dir): os.makedirs(asset_dir)
                male = self.img.crop(self.rects[0])
                female = self.img.crop(self.rects[1])
                male.save(os.path.join(asset_dir, "male.png"))
                female.save(os.path.join(asset_dir, "female.png"))
                self.log_func(f"✅ SUCCESS: Icons saved.")

            with open(CONFIG_PATH, "w") as f: json.dump(config, f, indent=4)
        except Exception as e:
            self.log_func(f"❌ Error saving: {e}")
            
        self.root.destroy()

def run_calibration(mode, log_func):
    # Damos un pequeño respiro para que el usuario cambie de ventana
    time.sleep(1)
    # Ejecutamos la clase de Tkinter
    selector = TkSelector(mode, log_func)
    # No llamamos a mainloop() aquí porque ya hay uno corriendo en main_gui.py
    # Pero root.wait_window() sirve para pausar el hilo hasta que se cierre
    selector.root.wait_window()
