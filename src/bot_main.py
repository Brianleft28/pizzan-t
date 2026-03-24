import cv2
import time
import json
import os
import requests
import random
import numpy as np
import re
from datetime import datetime
from threading import Thread
from src.vision import PokéObserver
from src.recognizer import PokéRecognizer
from src.controller import PokéController

class ShinyBot:
    def __init__(self, log_callback=None):
        self.running = False
        self.log_callback = log_callback if log_callback else print
        try:
            self.config = self.load_config()
            self.observer = PokéObserver()
            self.recognizer = PokéRecognizer()
            self.controller = PokéController(self.config, log_callback=self.log_callback)
            self.encounters = int(self.config.get("total_encounters", 0))
            self.encounters_since_leppa = 0
            self.log_callback("\n" + r"""
   ____  ____  ____  _____ _   _ 
  / ___|/ __ \|  _ \| ____| \ | |
  \___ \ |  | | |_) |  _| |  \| |
   ___) | |__| |  _ <| |___| |\  |
  |____/ \____/|_| \_\_____|_| \_|
  >> THE HUMANOID HUNTER IS ONLINE <<
            """ + "\n")
        except Exception as e: 
            self.log(f"ERROR: Initialization failed: {e}")

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f: return json.load(f)
        return {}

    def log(self, message, category="INFO"):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_callback(f"[{now}] [{category}] {message}")

    def is_ui_present(self, frame):
        """Detects HUD presence using HUD-specific elements (Menu, PPs)."""
        if self.is_menu_present(frame): return True
        pp_slots = self.config.get("pp_slots", {})
        if pp_slots:
            for i in range(1, 5):
                r = pp_slots.get(f"slot_{i}")
                if r:
                    crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
                    if cv2.countNonZero(thresh) > 20: return True
        slots = self.config.get("slots", {})
        for s_id, r in slots.items():
            crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 80: return True
        r_single = self.config.get("slot_single")
        if not r_single and slots: r_single = list(slots.values())[0]
        if r_single:
            crop = frame[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 100: return True
        return False

    def is_hp_low(self, frame):
        """Strict HP detection to ignore gold backgrounds."""
        r = self.config.get("hp_bar_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, np.array([40, 100, 100]), np.array([80, 255, 255]))
        mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([35, 255, 255]))
        total_px = crop.shape[0] * crop.shape[1]
        health_px = cv2.countNonZero(mask_green) + cv2.countNonZero(mask_yellow)
        percent = (health_px / total_px)
        return percent < 0.05

    def is_asleep(self, frame):
        """Detects sleep icon (Bilingual)."""
        r = self.config.get("status_slot_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        if self.recognizer.check_status_sleep(crop): return True
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = "".join([rm[1].upper() for rm in res])
        return any(x in txt for x in ["SLP", "DOR", "ZZ", "SLEEP"])

    def is_menu_present(self, frame):
        """Verifies if the battle menu is visible with OCR fallback."""
        btn_run = self.config.get("button_run")
        if not btn_run: return False
        menu_zone = frame[btn_run['y1']:btn_run['y2'], btn_run['x1']:btn_run['x2']]
        gray = cv2.cvtColor(menu_zone, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        px = cv2.countNonZero(thresh)
        if px > 100:
            res = self.recognizer.reader.readtext(cv2.convertScaleAbs(gray, alpha=1.2))
            txt = " ".join([rm[1].lower() for rm in res])
            keywords = ["huid", "huir", "run", "ida", "ata", "bat", "bol", "fight", "luc", "pkmn", "poke", "bag"]
            if any(k in txt for k in keywords): return True
        return False

    def read_pp(self, frame, slot_idx, move_name="Move"):
        """Reads PP and determines if restoration is efficient (Gap >= 10)."""
        pp_slots = self.config.get("pp_slots", {})
        slot_key = f"slot_{slot_idx}"
        if slot_key not in pp_slots: return 99, False
        r = pp_slots[slot_key]
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        res = self.recognizer.reader.readtext(upscaled)
        txt = " ".join([rm[1] for rm in res]).upper()
        clean_txt = txt.replace('O', '0').replace('I', '1').replace('S', '5').replace('B', '8')
        nums = re.findall(r'(\d+)', clean_txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            diff = total - curr
            self.log(f"{move_name} -> {curr}/{total} (Gap: {diff})")
            return curr, (diff >= 10)
        elif len(nums) == 1:
            curr = int(nums[0])
            self.log(f"{move_name} -> {curr}/?? (Partial read)")
            return curr, (curr <= 2)
        return 99, False

    def analyze_message(self, frame):
        """Analyzes battle message for success or failure (Bilingual)."""
        r = self.config.get("battle_msg_region")
        if not r: return None
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = " ".join([rm[1].lower() for rm in res])
        if not txt.strip(): return None
        success_keys = ["caught", "atrapado", "gotcha", "atrapó", "felicidades", "sent to", "box", "caja", "enviado"]
        failure_keys = ["broke", "free", "liberó", "escapó", "oh no", "fled", "shook"]
        if any(k in txt for k in success_keys): return "SUCCESS"
        if any(k in txt for k in failure_keys): return "FAILURE"
        return txt

    def loop(self):
        mode = self.config.get("mode", "horda")
        ocr_retries_config = int(self.config.get("ocr_retries", 6))
        ditto_ocr_retries = int(self.config.get("ditto_ocr_retries", 1))
        self.log_callback(f"\n╔══════════════════════════════════════════╗")
        self.log_callback(f"║  STARTING HUNT IN {mode.upper()} MODE   ║")
        self.log_callback(f"╚══════════════════════════════════════════╝\n")
        ditto_dir = 'right'; patrol_duration = float(self.config.get("ditto_patrol_time", 2.5))

        while self.running:
            frame = self.observer.capture_frame()
            if frame is None: continue

            # --- 1. STATE: MAP ---
            if not self.is_ui_present(frame):
                self.log(f"Starting Fluid Patrol: {ditto_dir.upper()}", "MAP")
                self.controller.key_down(ditto_dir)
                patrol_start = time.time(); encounter_found = False
                while (time.time() - patrol_start) < patrol_duration:
                    if not self.running: break
                    if self.is_ui_present(self.observer.capture_frame()):
                        encounter_found = True; break
                    time.sleep(0.05)
                self.controller.key_up(ditto_dir)
                if not encounter_found:
                    ditto_dir = 'left' if ditto_dir == 'right' else 'right'
                    base_time = float(self.config.get("ditto_patrol_time", 2.5)) if mode == "ditto" else 3.0
                    patrol_duration = base_time * random.uniform(0.8, 1.2)
                    continue
                else: self.log("Encounter triggered!", "INFO")
                for _ in range(15): 
                    time.sleep(0.1)
                    if self.is_ui_present(self.observer.capture_frame()): break
                if not self.is_ui_present(self.observer.capture_frame()): continue

            # --- 2. STATE: BATTLE ---
            menu_ready = False
            for i in range(30): 
                if self.is_menu_present(self.observer.capture_frame()): menu_ready = True; break
                time.sleep(0.15)
            if menu_ready: time.sleep(1.2)

            # --- 3. STATE: ANALYSIS ---
            shiny_found = False; is_horde_detected = False
            if mode == "ditto":
                hunter_name = self.config.get("hunter_pokemon_name", "Magikarp").lower()
                is_ditto = False
                for attempt in range(max(1, ditto_ocr_retries)):
                    frame_battle = self.observer.capture_frame()
                    r_single = self.config.get("slot_single")
                    if not r_single: r_single = list(self.config.get("slots", {}).values())[0]
                    res = self.recognizer.analyze_slot(frame_battle[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']])
                    name = res['name'].lower().strip()
                    if res['is_shiny']: shiny_found = True; self.log("SHINY DITTO!", "!!!"); break
                    self.log(f"OCR Check: '{name}'", "DEBUG")
                    if any(x in name for x in ["ditto", "itto", "ditt", "ito"]):
                        is_ditto = True; self.log("DITTO CONFIRMED!", "SUCCESS"); break
                    if hunter_name in name and len(name) > 2: is_ditto = True; break
                    if len(name) > 3 and not is_ditto: break
                    time.sleep(0.8)
                
                if not shiny_found and is_ditto:
                    # --- CATCHING SEQUENCE ---
                    is_soaked = False; has_swiped = False; turn_count = 1; slots_needing_leppa = set()
                    while self.running:
                        frame_battle = self.observer.capture_frame()
                        if not self.is_menu_present(frame_battle):
                            msg = self.analyze_message(frame_battle)
                            if msg == "SUCCESS": self.log("CAPTURE CONFIRMED!", "SUCCESS"); break
                            time.sleep(0.5); continue

                        asleep = self.is_asleep(frame_battle); low_hp = self.is_hp_low(frame_battle) or has_swiped
                        self.log_callback(f"  [ TURN {turn_count} ] HP:{'[LOW]' if low_hp else '[HI]'} ST:{'[SLP]' if asleep else '[AWK]'}")
                        
                        target_slot = None; target_name = ""
                        if not has_swiped: 
                            target_slot = self.config.get("ditto_key_attack", "2"); target_name = self.config.get("ditto_name_attack", "Swipe")
                        elif not is_soaked: 
                            target_slot = self.config.get("ditto_key_soak", "4"); target_name = self.config.get("ditto_name_soak", "Soak")
                        elif not asleep: 
                            target_slot = self.config.get("ditto_key_sleep", "1"); target_name = self.config.get("ditto_name_sleep", "Sleep")
                        
                        if target_slot:
                            self.controller.open_fight_menu(); time.sleep(0.6)
                            pp_curr, needs_restore = self.read_pp(self.observer.capture_frame(), target_slot, target_name)
                            if needs_restore: slots_needing_leppa.add(target_slot)
                            self.controller.navigate_and_confirm_move(target_slot)
                            if not has_swiped and target_name == self.config.get("ditto_name_attack", "Swipe"): has_swiped = True
                            if not is_soaked and target_name == self.config.get("ditto_name_soak", "Soak"): is_soaked = True
                        else:
                            self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                            success_detected = False
                            for _ in range(35): 
                                fm = self.observer.capture_frame()
                                m = self.analyze_message(fm)
                                if m == "SUCCESS": self.log("CAPTURE CONFIRMED!", "SUCCESS"); success_detected = True; break
                                elif m == "FAILURE": self.log("Capture failed. Resuming cycle.", "INFO"); break
                                if not self.is_ui_present(fm) and not self.is_menu_present(fm):
                                    time.sleep(1.0)
                                    if not self.is_ui_present(self.observer.capture_frame()): success_detected = True; break
                                time.sleep(0.2)
                            if success_detected: 
                                self.log("Capture confirmed! Clearing post-capture menus...", "SUCCESS")
                                # Spam 'X' to close nickname prompts, summaries and PC notifications
                                for _ in range(6):
                                    self.controller._press('x')
                                    time.sleep(0.8)
                                break
                        time.sleep(6.5); turn_count += 1
                    
                    self.encounters += 1; self.save_progress()
                    if slots_needing_leppa:
                        # Safety: Double confirm we are out of combat
                        time.sleep(2.5)
                        if not self.is_ui_present(self.observer.capture_frame()):
                            leppa_key = self.config.get("ditto_key_leppa", "4")
                            potion_key = self.config.get("ditto_key_potion", "6")
                            self.log("Restoring HP/PP out of combat...", "ACTION")
                            self.controller._press(potion_key, duration=0.4) # Heal hunter
                            time.sleep(1.5)
                            for s in slots_needing_leppa: self.controller.use_leppa_sequence_single(leppa_key, s)
                    continue 
                elif not shiny_found: self.log("Not Ditto.", "INFO")

            else:
                # Horde / Single logic...
                for attempt in range(ocr_retries_config):
                    frame_battle = self.observer.capture_frame()
                    total_id = 0; slots = self.config.get("slots", {})
                    for s_id, r in slots.items():
                        res = self.recognizer.analyze_slot(frame_battle[r['y1']:r['y2'], r['x1']:r['x2']])
                        if res['name']: total_id += 1; self.log_callback(f"   [#] {s_id.upper()}: {res['name']}")
                        if res['is_shiny']: shiny_found = True; break
                    if total_id >= 3: is_horde_detected = True
                    if not shiny_found and mode == "single" and not is_horde_detected:
                        r_single = self.config.get("slot_single")
                        if r_single:
                            res = self.recognizer.analyze_slot(frame_battle[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']])
                            if res['name']: total_id += 1; self.log_callback(f"   [#] SINGLE: {res['name']}")
                            if res['is_shiny']: shiny_found = True
                    if shiny_found or total_id > 0: break
                    time.sleep(1)

            if shiny_found:
                self.log_callback("\n✨✨✨ SHINY DETECTED! ✨✨✨\n")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.send_discord_alert("BATTLE", "SHINY!", "shiny_detected.png")
                self.running = False; break

            # --- 4. STATE: ESCAPE ---
            escape_success = False
            for attempt in range(3):
                if not self.is_ui_present(self.observer.capture_frame()): escape_success = True; break
                self.controller.run_away()
                map_stable = 0
                for _ in range(15): 
                    time.sleep(0.15)
                    if not self.is_ui_present(self.observer.capture_frame()): map_stable += 1
                    else: map_stable = 0
                    if map_stable >= 2: escape_success = True; break
                if escape_success: break
            if escape_success:
                self.encounters += 1
                self.log_callback(f"  📊 TOTAL ENCOUNTERS: [ {self.encounters} ]")
                self.save_progress()

    def send_discord_alert(self, slot, name, img_path):
        url = self.config.get("discord_webhook")
        if not url: return
        try:
            with open(img_path, "rb") as f:
                requests.post(url, data={"content": f"🏆 SHINY FOUND! {name} in {slot}"}, files={"file": f})
        except: pass

    def save_progress(self):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: cfg = json.load(f)
                cfg["total_encounters"] = self.encounters
                with open("config.json", "w") as f: json.dump(cfg, f, indent=4)
        except: pass

    def start(self):
        self.running = True
        self.thread = Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False; self.save_progress()
