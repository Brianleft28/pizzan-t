import cv2
import time
import json
import os
import requests
import random
import numpy as np
import re
from datetime import datetime, timedelta
from threading import Thread
from src.vision import PokéObserver
from src.recognizer import PokéRecognizer
from src.controller import PokéController

class ShinyBot:
    def __init__(self, log_callback=None):
        self.running = False
        self.log_callback = log_callback if log_callback else print
        self.ditto_dir = random.choice(['left', 'right'])
        self.start_time = None
        try:
            self.config = self.load_config()
            self.observer = PokéObserver()
            self.recognizer = PokéRecognizer()
            self.controller = PokéController(self.config, log_callback=self.log_callback)
            self.encounters = int(self.config.get("total_encounters", 0))
            self.log_callback("\n" + r"""
    ███████╗ ██████╗ ██████╗ ███████╗███╗   ██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗  ██║
    ███████╗██║   ██║██████╔╝█████╗  ██╔██╗ ██║
    ╚════██║██║   ██║██╔══██╗██╔══╝  ██║╚██╗██║
    ███████║╚██████╔╝██║  ██║███████╗██║ ╚████║
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝
    >> THE HUMANOID HUNTER v2.2 - DATA DRIVEN <<
            """ + "\n")
        except Exception as e: 
            self.log(f"ERROR: Initialization failed: {e}")

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f: return json.load(f)
        return {}

    def get_elapsed_time(self):
        if not self.start_time: return "00:00:00"
        elapsed = datetime.now() - self.start_time
        return str(timedelta(seconds=int(elapsed.total_seconds())))

    def log(self, message, category="INFO"):
        timer = self.get_elapsed_time()
        self.log_callback(f"[{timer}] [{category}] {message}")

    def is_slot_active(self, frame):
        """Fast check if the Pokemon Name Slot has light pixels (text)."""
        r = self.config.get("slot_single")
        if not r: 
            slots = self.config.get("slots", {})
            if slots: r = list(slots.values())[0]
        if not r: return False
        
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        return cv2.countNonZero(thresh) > 50

    def is_menu_present(self, frame):
        """Checks for the Run/Fight button."""
        btn_run = self.config.get("button_run")
        if not btn_run: return False
        menu_zone = frame[btn_run['y1']:btn_run['y2'], btn_run['x1']:btn_run['x2']]
        gray = cv2.cvtColor(menu_zone, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        return cv2.countNonZero(thresh) > 100

    def read_hunter_hp(self, frame):
        r = self.config.get("hunter_hp_region")
        if not r: return False, "??/??"
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY); upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        res = self.recognizer.reader.readtext(upscaled)
        txt = "".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1')
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            return (total - curr) >= 60, f"{curr}/{total}"
        return False, txt if txt.strip() else "??/??"

    def is_hp_low(self, frame):
        r = self.config.get("hp_bar_region")
        if not r: return False, 0.0
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, np.array([40, 100, 100]), np.array([80, 255, 255]))
        mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([35, 255, 255]))
        health_px = cv2.countNonZero(mask_green) + cv2.countNonZero(mask_yellow)
        percent = (health_px / (crop.shape[0] * crop.shape[1]))
        return percent < 0.05, percent

    def is_asleep(self, frame):
        r = self.config.get("status_slot_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        if self.recognizer.check_status_sleep(crop): return True
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = "".join([rm[1].upper() for rm in res])
        return any(x in txt for x in ["SLP", "DOR", "ZZ", "SLEEP"])

    def check_capture_success(self, frame):
        r = self.config.get("battle_msg_region")
        if not r: return None
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = " ".join([rm[1].lower() for rm in res])
        success = ["caught", "atrapado", "gotcha", "atrapó", "sent to", "box", "caja"]
        if any(k in txt for k in success): return "SUCCESS"
        return "FAILURE" if any(k in txt for k in ["broke", "free", "liberó", "escapó"]) else None

    def loop(self):
        mode = self.config.get("mode", "horda")
        self.start_time = datetime.now()
        self.log_callback(f"\n╔══════════════════════════════════════════╗\n║  SYSTEM ONLINE: {mode.upper()} MODE  ║\n╚══════════════════════════════════════════╝\n")
        
        while self.running:
            frame = self.observer.capture_frame()
            if frame is None: continue

            # --- 1. PATROL STATE ---
            if not self.is_slot_active(frame) and not self.is_menu_present(frame):
                self.log(f"PATROLLING: {self.ditto_dir.upper()}", "MAP")
                burst = random.uniform(0.6, 1.2)
                self.controller.key_down(self.ditto_dir)
                st = time.time(); encounter = False
                while (time.time() - st) < burst:
                    if not self.running: break
                    f_now = self.observer.capture_frame()
                    if self.is_slot_active(f_now): encounter = True; break
                    time.sleep(0.05)
                self.controller.key_up(self.ditto_dir)
                if not encounter:
                    if random.random() > 0.5: self.ditto_dir = 'left' if self.ditto_dir == 'right' else 'right'
                    continue
                else: self.log(">>> BATTLE GATE TRIGGERED!", "BRAIN")

            # --- 2. VERIFICATION STATE ---
            self.log("Waiting for Pokemon confirmation...", "BRAIN")
            target_confirmed = False; is_shiny = False; target_name = ""
            
            # Wait for name to stabilize and OCR
            for _ in range(10):
                f_ocr = self.observer.capture_frame()
                res = self.recognizer.analyze_slot(f_ocr)
                if res['name']:
                    target_name = res['name']
                    self.log(f"DETECTED: '{target_name.upper()}'", "BATTLE")
                    if res['is_shiny']: is_shiny = True; break
                    if any(x in target_name.lower() for x in ["ditto", "itto", "ditt", "ito"]): target_confirmed = True; break
                    if mode != "ditto" and len(target_name) > 2: target_confirmed = True; break
                time.sleep(0.3)

            # Wait for Menu to be ready to act
            self.log("Waiting for Menu stability...", "BRAIN")
            menu_ready = False
            for _ in range(30):
                if self.is_menu_present(self.observer.capture_frame()): menu_ready = True; break
                time.sleep(0.1)
            
            if not menu_ready:
                self.log("No menu found. Likely a false positive. Resuming patrol.", "DEBUG")
                continue

            # --- 3. DECISION STATE ---
            if is_shiny:
                self.log_callback("\n✨✨✨ SHINY DETECTED! ✨✨✨")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.send_discord_alert("BATTLE", f"SHINY {target_name}!", "shiny_detected.png")
                target_confirmed = True # Catch it!

            if target_confirmed:
                self.log(f"INITIATING CAPTURE FOR {target_name.upper()}", "ACTION")
                is_soak = False; is_swiped = False; turn = 1; leppa_slots = set(); needs_pot = False
                while self.running:
                    f_bat = self.observer.capture_frame()
                    if not self.is_menu_present(f_bat):
                        if self.check_capture_success(f_bat) == "SUCCESS": self.log("CAPTURED!", "SUCCESS"); break
                        time.sleep(2.0)
                        if not self.is_ui_present(self.observer.capture_frame()): break
                        continue
                    
                    slp = self.is_asleep(f_bat); low, hp_p = self.is_hp_low(f_bat); low = low or is_swiped
                    pot, h_hp = self.read_hunter_hp(f_bat); if pot: needs_pot = True
                    
                    self.log_callback(f"┌─ TURN {turn:02d} ────────────────────────┐")
                    self.log_callback(f"│ Target: {hp_p:.1%} HP | {'[SLP]' if slp else '[AWK]'} | My HP: {h_hp}")
                    self.log_callback(f"└────────────────────────────────┘")
                    
                    mv_s = None; mv_n = ""
                    if not low: mv_s = self.config.get("ditto_key_attack", "2"); mv_n = "Swipe"
                    elif not is_soak: mv_s = self.config.get("ditto_key_soak", "4"); mv_n = "Soak"
                    elif not slp: mv_s = self.config.get("ditto_key_sleep", "1"); mv_n = "Sleep"
                    
                    if mv_s:
                        self.controller.open_fight_menu(); time.sleep(0.4)
                        self.controller.navigate_and_confirm_move(mv_s)
                        if mv_n == "Swipe": is_swiped = True
                        if mv_n == "Soak": is_soak = True
                        time.sleep(4.0)
                    else:
                        self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                        success = False
                        for _ in range(40): 
                            res = self.check_capture_success(self.observer.capture_frame())
                            if res == "SUCCESS": success = True; break
                            elif res == "FAILURE": break
                            if not self.is_ui_present(self.observer.capture_frame()): break
                            time.sleep(0.2)
                        if success: break
                    turn += 1
                
                self.encounters += 1; self.save_progress()
                for _ in range(3): self.controller._press('x'); time.sleep(0.5)
                if leppa_slots or needs_pot:
                    time.sleep(3.0); self.log("RESTORING HP/PP...", "ACTION")
                    if needs_pot: self.controller.use_potion_sequence(self.config.get("ditto_key_potion", "6"), True); time.sleep(1.0)
                    for s in leppa_slots: self.controller.use_leppa_sequence_single(self.config.get("ditto_key_leppa", "4"), s[0], s[1])
                continue 

            # --- 4. ESCAPE STATE (If not target) ---
            self.log(f"Target '{target_name}' not in list. Escaping.", "INFO")
            self.controller.run_away()
            time.sleep(2.0); self.encounters += 1; self.save_progress()
            self.log(f"TOTAL ENCOUNTERS: [ {self.encounters} ]", "STATS")

    def send_discord_alert(self, slot, name, img_path):
        url = self.config.get("discord_webhook")
        if not url: return
        try:
            with open(img_path, "rb") as f: requests.post(url, data={"content": f"🏆 SHINY FOUND! {name} in {slot}"}, files={"file": f})
        except: pass

    def save_progress(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: cfg = json.load(f)
                cfg["total_encounters"] = self.encounters
                with open("config.json", "w") as f: json.dump(cfg, f, indent=4)
        except: pass

    def start(self):
        self.running = True; self.thread = Thread(target=self.loop, daemon=True); self.thread.start()

    def stop(self):
        self.running = False; self.save_progress()
