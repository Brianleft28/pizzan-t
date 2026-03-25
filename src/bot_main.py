import cv2
import time
import json
import os
import requests
import random
import numpy as np
from datetime import datetime, timedelta
from threading import Thread
from src.vision import PokéObserver
from src.recognizer import PokéRecognizer
from src.controller import PokéController
from src.logger import PokéLogger

# Importar los modos
from src.modes.horda import HordeMode
from src.modes.ditto import DittoMode
from src.modes.single import SingleMode

class ShinyBot:
    def __init__(self, log_widget=None):
        self.running = False
        self.start_time = None
        self.last_action_time = time.time()
        
        # Clase Logger independiente
        self.logger = PokéLogger(log_widget)
        self.log_callback = self.logger.log # Mantener compatibilidad si se usa como callback
        
        try:
            self.config = self.load_config()
            self.observer = PokéObserver()
            self.recognizer = PokéRecognizer()
            self.controller = PokéController(self.config, log_callback=self.log_callback)
            self.encounters = int(self.config.get("total_encounters", 0))
            
            self.mode_instance = self._initialize_mode()
            
            self.logger.log("---------------------------------------")
            self.logger.log("  THE HUMANOID HUNTER v6.5 - PRO      ", "SUCCESS")
            self.logger.log("---------------------------------------")
        except Exception as e: 
            self.logger.log(f"Bot initialization failed: {e}", "FATAL")

    def _initialize_mode(self):
        mode_name = self.config.get("mode", "horda").lower()
        if mode_name == "horda": return HordeMode(self)
        if mode_name == "ditto": return DittoMode(self)
        if mode_name == "single": return SingleMode(self)
        return HordeMode(self)

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f: return json.load(f)
        return {}

    def save_progress(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: cfg = json.load(f)
                cfg["total_encounters"] = self.encounters
                with open("config.json", "w") as f: json.dump(cfg, f, indent=4)
        except: pass

    def get_elapsed_time(self):
        if not self.start_time: return "00:00:00"
        elapsed = datetime.now() - self.start_time
        return str(timedelta(seconds=int(elapsed.total_seconds())))

    def log(self, message, category="INFO"):
        self.logger.log(message, category)

    # --- Visión ---
    def is_menu_ready(self, frame):
        r = self.config.get("button_run")
        if not r or frame is None: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = " ".join([rm[1].lower() for rm in res])
        keywords = ["run", "huir", "huida", "fight", "luch", "bag", "moch", "pkmn", "poke", "ata", "batalla", "combate", "escapar"]
        return any(k in txt for k in keywords)

    def get_slot_data(self, frame, region):
        crop = frame[region['y1']:region['y2'], region['x1']:region['x2']]
        return self.recognizer.analyze_slot(crop)

    def check_any_name_visible(self, frame):
        if frame is None: return False
        h_slots = self.config.get("slots", {})
        for s_id, r in h_slots.items():
            res = self.get_slot_data(frame, r)
            if res['name'] and len(res['name']) > 2: return True
        r_s = self.config.get("slot_single")
        if r_s:
            res_s = self.get_slot_data(frame, r_s)
            if res_s['name'] and len(res_s['name']) > 2: return True
        return False

    def is_hp_low(self, frame):
        r = self.config.get("hp_bar_region")
        if not r or frame is None: return False, 0.0
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_g = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([90, 255, 255]))
        mask_y = cv2.inRange(hsv, np.array([15, 50, 50]), np.array([35, 255, 255]))
        g_px = cv2.countNonZero(mask_g); y_px = cv2.countNonZero(mask_y)
        percent = (g_px + y_px) / (crop.shape[0] * crop.shape[1] + 1e-6)
        return (g_px + y_px) < 15, percent

    def is_asleep(self, frame):
        r = self.config.get("status_slot_region")
        if not r or frame is None: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        return self.recognizer.check_status_sleep(crop)

    def read_hunter_hp(self, frame):
        r = self.config.get("hunter_hp_region")
        if not r or frame is None: return False, "??/??", 0
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        res = self.recognizer.reader.readtext(gray)
        txt = "".join([rm[1] for rm in res]).upper()
        import re
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            gap = total - curr
            return (gap >= 60), f"{curr}/{total}", gap
        return False, "??/??", 0

    def read_pp(self, frame, slot_idx, move_name="Move"):
        pp_slots = self.config.get("pp_slots", {})
        slot_key = f"slot_{slot_idx}"
        if slot_key not in pp_slots or frame is None: return 99, False
        r = pp_slots[slot_key]
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = "".join([rm[1] for rm in res]).upper()
        import re
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            return curr, (total - curr >= 10)
        return 99, False

    def check_msg_area(self, frame):
        r = self.config.get("battle_msg_region")
        if not r or frame is None: return None
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = " ".join([rm[1].lower() for rm in res])
        success = ["caught", "atrapado", "gotcha", "sent to", "caja", "enviado"]
        if any(k in txt for k in success): return "SUCCESS"
        if any(k in txt for k in ["broke", "free", "liberó", "escapó", "oh no"]): return "FAILURE"
        return None

    def send_discord_alert(self, category, message, img_path):
        url = self.config.get("discord_webhook")
        if url:
            try:
                with open(img_path, "rb") as f:
                    requests.post(url, data={"content": f"🏆 {category}: {message}"}, files={"file": f})
            except: pass

    def loop(self):
        self.start_time = datetime.now()
        self.logger.clear_start_time()
        self.last_action_time = time.time()
        
        while self.running:
            try:
                frame = self.observer.capture_frame()
                if frame is None: continue

                if time.time() - self.last_action_time > 45:
                    self.log("SENTINEL: Anti-stuck triggered!", "WARN")
                    for _ in range(3): self.controller._press('x'); time.sleep(0.5)
                    self.last_action_time = time.time()

                self.mode_instance.execute(frame)
                self.last_action_time = time.time()
                time.sleep(0.1)
            except Exception as e:
                self.log(f"LOOP ERROR: {e}", "FATAL")
                time.sleep(1.0)

    def start(self):
        self.running = True
        self.thread = Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.save_progress()
