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
    >> THE HUMANOID HUNTER v4.6 - EARLY TRIGGER <<
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

    def is_menu_ready(self, frame):
        """Action Anchor: Confirms turn using RUN button area."""
        r = self.config.get("button_run")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = " ".join([rm[1].lower() for rm in res])
        keywords = ["run", "huir", "huida", "fight", "luch", "bag", "moch", "pkmn", "poke", "ata", "batalla", "combate", "escapar"]
        return any(k in txt for k in keywords)

    def get_slot_data(self, frame, region):
        """Helper to OCR a specific region."""
        crop = frame[region['y1']:region['y2'], region['x1']:region['x2']]
        return self.recognizer.analyze_slot(crop)

    def check_msg_area(self, frame):
        """Active OCR on message region for capture verification."""
        r = self.config.get("battle_msg_region")
        if not r: return None
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = " ".join([rm[1].lower() for rm in res])
        if txt.strip(): self.log(f"Msg OCR: '{txt.upper()}'", "DEBUG")
        success = ["caught", "atrapado", "gotcha", "sent to", "caja", "enviado"]
        if any(k in txt for k in success): return "SUCCESS"
        if any(k in txt for k in ["broke", "free", "liberó", "escapó"]): return "FAILURE"
        return None

    def read_hunter_hp(self, frame):
        r = self.config.get("hunter_hp_region")
        if not r: return False, "??/??"
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY); upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        res = self.recognizer.reader.readtext(upscaled)
        txt = "".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1')
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1]); gap = total - curr
            return (gap >= 60), f"{curr}/{total}", gap
        return False, "??/??", 0

    def is_hp_low(self, frame):
        r = self.config.get("hp_bar_region")
        if not r: return False, 0.0
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_g = cv2.inRange(hsv, np.array([35, 50, 50]), np.array([90, 255, 255]))
        mask_y = cv2.inRange(hsv, np.array([15, 50, 50]), np.array([35, 255, 255]))
        g_px = cv2.countNonZero(mask_g); y_px = cv2.countNonZero(mask_y)
        percent = (g_px + y_px) / (crop.shape[0] * crop.shape[1])
        return (g_px + y_px) < 15, percent

    def is_asleep(self, frame):
        r = self.config.get("status_slot_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        return self.recognizer.check_status_sleep(crop)

    def read_pp(self, frame, slot_idx, move_name="Move"):
        pp_slots = self.config.get("pp_slots", {})
        slot_key = f"slot_{slot_idx}"
        if slot_key not in pp_slots: return 99, False
        r = pp_slots[slot_key]
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = "".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1').replace('S', '5').replace('B', '8')
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1]); gap = total - curr
            self.log(f"{move_name} PP: {curr}/{total} (Gap: {gap})")
            return curr, (gap >= 10)
        return 99, False

    def loop(self):
        mode = self.config.get("mode", "horda").lower()
        self.start_time = datetime.now()
        self.log_callback(f"\n╔══════════════════════════════════════════╗\n║  SYSTEM v4.6 EARLY TRIGGER: {mode.upper()}  ║\n╚══════════════════════════════════════════╝\n")
        
        while self.running:
            frame = self.observer.capture_frame()
            if frame is None: continue

            # --- 1. PATROL (Trigger: Any text in Single Slot) ---
            r_s = self.config.get("slot_single")
            # If no menu and no name, walk
            if not self.is_menu_ready(frame) and not self.get_slot_data(frame, r_s)['name']:
                self.log(f"PATROLLING: {self.ditto_dir.upper()}", "MAP")
                burst = random.uniform(0.6, 1.2); self.controller.key_down(self.ditto_dir)
                st = time.time(); encounter = False
                while (time.time() - st) < burst:
                    if not self.running: break
                    # EARLY TRIGGER: Scan name slot to stop walk immediately
                    if self.get_slot_data(self.observer.capture_frame(), r_s)['name']:
                        encounter = True; break
                    time.sleep(0.05)
                self.controller.key_up(self.ditto_dir)
                if not encounter:
                    if random.random() > 0.5: self.ditto_dir = 'left' if self.ditto_dir == 'right' else 'right'
                    continue
                else: self.log(">>> NAME DETECTED! STOPPING PATROL.", "BRAIN")

            # --- 2. BATTLE WAIT (Wait for menu) ---
            while self.running and not self.is_menu_ready(self.observer.capture_frame()):
                time.sleep(0.1)

            # --- 3. UNIVERSAL SCAN ---
            f_bat = self.observer.capture_frame()
            shiny_found = False; shiny_name = ""; is_horde = False; is_target = False; target_name = ""
            
            h_slots = self.config.get("slots", {})
            h_count = 0
            for s_id, r in h_slots.items():
                res = self.get_slot_data(f_bat, r)
                if res['name']: 
                    h_count += 1
                    if res['is_shiny']: shiny_found = True; shiny_name = res['name']; break
            if h_count >= 3: is_horde = True
            
            res_s = self.get_slot_data(f_bat, r_s)
            if res_s['name'] and not shiny_found:
                self.log(f"Detected: {res_s['name']}", "BATTLE")
                if res_s['is_shiny']: shiny_found = True; shiny_name = res_s['name']
                else:
                    if mode == "ditto" and any(x in res_s['name'].lower() for x in ["ditto", "itto", "ditt", "ito"]): is_target = True; target_name = "Ditto"
                    elif mode == "single" and len(res_s['name']) > 2: is_target = True; target_name = res_s['name']

            if shiny_found:
                self.log_callback("\n✨✨✨ SHINY DETECTED: " + shiny_name.upper() + " ✨✨✨")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.send_discord_alert("BATTLE", f"SHINY {shiny_name}!", "shiny_detected.png")
                if is_horde:
                    self.log("SHINY IN HORDE! MANUAL REQ.", "FATAL"); self.running = False; break
                else: is_target = True; target_name = shiny_name

            # --- 4. COMBAT ---
            if is_target:
                self.log(f"INITIATING CAPTURE FOR {target_name.upper()}", "ACTION")
                turn = 1; swiped = False; soaked = False; needs_pot = False; leppas = set()
                while self.running:
                    while self.running:
                        f_turn = self.observer.capture_frame()
                        if self.is_menu_ready(f_turn): break
                        # End detection: Menu gone for 6s (default)
                        if not self.is_menu_ready(f_turn):
                            timeout_s = float(self.config.get("battle_end_timeout", 6.0))
                            start_ver = time.time(); ended = True
                            while (time.time() - start_ver) < timeout_s:
                                if self.is_menu_ready(self.observer.capture_frame()):
                                    ended = False; break
                                time.sleep(0.2)
                            if ended: break 
                        time.sleep(0.2)
                    
                    if not self.is_menu_ready(self.observer.capture_frame()): break

                    f_act = self.observer.capture_frame()
                    slp = self.is_asleep(f_act)
                    low, hp_p = self.is_hp_low(f_act); low = low or swiped
                    pot_n, h_hp, hp_g = self.read_hunter_hp(f_act); 
                    if pot_n: needs_pot = True
                    
                    self.log_callback(f"┌─ TURN {turn:02d} ── Target: {hp_p:.1%} HP | {'[SLP]' if slp else '[AWK]'} | My HP: {h_hp}")
                    
                    mv_s = self.config.get("ditto_key_attack", "2") if not low else \
                           self.config.get("ditto_key_soak", "4") if not soaked else \
                           self.config.get("ditto_key_sleep", "1") if not slp else None
                    
                    if mv_s:
                        self.controller.open_fight_menu(); time.sleep(0.5)
                        _, nr = self.read_pp(self.observer.capture_frame(), mv_s, "MOVE")
                        if nr: leppas.add((mv_s, True))
                        self.controller.navigate_and_confirm_move(mv_s)
                        if not low: swiped = True
                        elif not soaked: soaked = True
                        time.sleep(1.0)
                        while self.is_menu_ready(self.observer.capture_frame()) and self.running: time.sleep(0.2)
                    else:
                        self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                        cap_confirmed = False
                        for _ in range(60): 
                            f_ball = self.observer.capture_frame()
                            m_status = self.check_msg_area(f_ball)
                            if m_status == "SUCCESS": cap_confirmed = True; break
                            if self.is_menu_ready(f_ball): break
                            time.sleep(0.1)
                        if cap_confirmed: self.log("CAPTURE CONFIRMED!", "SUCCESS"); break
                    turn += 1
                
                self.encounters += 1; self.save_progress()
                for _ in range(3): self.controller._press('x'); time.sleep(0.5)
                time.sleep(2.5) 
                if not self.is_menu_ready(self.observer.capture_frame()):
                    if needs_pot: self.controller.use_potion_sequence(self.config.get("ditto_key_potion", "6"), True); time.sleep(1.0)
                    for s in leppas: self.controller.use_leppa_sequence_single(self.config.get("ditto_key_leppa", "4"), s[0], s[1])
                continue

            self.log("Not desired. Escaping...", "INFO")
            self.controller.run_away()
            time.sleep(1.5); self.encounters += 1; self.save_progress()

    def send_discord_alert(self, slot, name, img_path):
        url = self.config.get("discord_webhook")
        if url:
            try:
                cv2.imwrite(img_path, self.observer.capture_frame())
                with open(img_path, "rb") as f: requests.post(url, data={"content": f"🏆 SHINY FOUND! {name}"}, files={"file": f})
            except: pass

    def save_progress(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: cfg = json.load(f); cfg["total_encounters"] = self.encounters
                with open("config.json", "w") as f: json.dump(cfg, f, indent=4)
        except: pass

    def start(self):
        self.running = True; self.thread = Thread(target=self.loop, daemon=True); self.thread.start()

    def stop(self):
        self.running = False; self.save_progress()
