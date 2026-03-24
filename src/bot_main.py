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
        self.ditto_dir = random.choice(['left', 'right'])
        try:
            self.config = self.load_config()
            self.observer = PokéObserver()
            self.recognizer = PokéRecognizer()
            self.controller = PokéController(self.config, log_callback=self.log_callback)
            self.encounters = int(self.config.get("total_encounters", 0))
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
        """Detects HUD presence using ONLY Pokemon slots (to avoid map noise)."""
        mode = self.config.get("mode", "horda")
        slots = self.config.get("slots", {})
        
        # Check Horde Slots (High threshold 230)
        horde_count = 0
        for s_id, r in slots.items():
            crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 60: horde_count += 1
        if horde_count >= 3: return True
        
        # Check Single/Ditto Slot
        r_single = self.config.get("slot_single")
        if not r_single and slots: r_single = list(slots.values())[0]
        if r_single:
            crop = frame[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 80: return True
            
        return False

    def is_hp_low(self, frame):
        r = self.config.get("hp_bar_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, np.array([40, 100, 100]), np.array([80, 255, 255]))
        mask_yellow = cv2.inRange(hsv, np.array([20, 100, 100]), np.array([35, 255, 255]))
        total_px = crop.shape[0] * crop.shape[1]
        health_px = cv2.countNonZero(mask_green) + cv2.countNonZero(mask_yellow)
        return (health_px / total_px) < 0.05

    def read_hunter_hp(self, frame):
        r = self.config.get("hunter_hp_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY); upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        res = self.recognizer.reader.readtext(upscaled)
        txt = " ".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1')
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            return (total - curr) >= 60
        return False

    def is_asleep(self, frame):
        r = self.config.get("status_slot_region")
        if not r: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        if self.recognizer.check_status_sleep(crop): return True
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = "".join([rm[1].upper() for rm in res])
        return any(x in txt for x in ["SLP", "DOR", "ZZ", "SLEEP"])

    def is_menu_present(self, frame):
        """Verifies battle menu with OCR backup (Threshold 160)."""
        btn_run = self.config.get("button_run")
        if not btn_run: return False
        menu_zone = frame[btn_run['y1']:btn_run['y2'], btn_run['x1']:btn_run['x2']]
        gray = cv2.cvtColor(menu_zone, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY)
        px = cv2.countNonZero(thresh)
        if px > 60:
            res = self.recognizer.reader.readtext(cv2.convertScaleAbs(gray, alpha=1.2))
            txt = " ".join([rm[1].lower() for rm in res])
            keywords = ["huid", "huir", "run", "ida", "ata", "bat", "bol", "fight", "luc", "pkmn", "poke", "bag"]
            if any(k in txt for k in keywords): return True
        return False

    def read_pp(self, frame, slot_idx, move_name="Move"):
        """Reads PP and returns (current, needs_restore)."""
        pp_slots = self.config.get("pp_slots", {})
        slot_key = f"slot_{slot_idx}"
        if slot_key not in pp_slots: return 99, False
        r = pp_slots[slot_key]
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY); upscaled = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        res = self.recognizer.reader.readtext(upscaled)
        txt = " ".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1').replace('S', '5').replace('B', '8')
        nums = re.findall(r'(\d+)', txt)
        if len(nums) >= 2:
            curr, total = int(nums[0]), int(nums[1])
            diff = total - curr
            self.log(f"{move_name} PP: {curr}/{total} (Gap: {diff})")
            return curr, (diff >= 10)
        elif len(nums) == 1:
            curr = int(nums[0]); return curr, (curr <= 2)
        return 99, False

    def check_capture_success(self, frame):
        r = self.config.get("battle_msg_region")
        if not r: return None
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY))
        txt = " ".join([rm[1].lower() for rm in res])
        if not txt.strip(): return None
        success = ["caught", "atrapado", "gotcha", "atrapó", "felicidades", "sent to", "box", "caja", "enviado"]
        failure = ["broke", "free", "liberó", "escapó", "oh no", "fled", "shook"]
        if any(k in txt for k in success): return "SUCCESS"
        if any(k in txt for k in failure): return "FAILURE"
        return txt

    def loop(self):
        mode = self.config.get("mode", "horda")
        ocr_retries_config = int(self.config.get("ocr_retries", 6))
        ditto_ocr_retries = int(self.config.get("ditto_ocr_retries", 1))
        self.log_callback(f"\n╔══════════════════════════════════════════╗\n║  STARTING HUNT IN {mode.upper()} MODE   ║\n╚══════════════════════════════════════════╝\n")
        patrol_duration = float(self.config.get("ditto_patrol_time", 2.5))

        while self.running:
            frame = self.observer.capture_frame()
            if frame is None: continue

            # --- 1. STATE: MAP ---
            if not self.is_ui_present(frame):
                if random.random() > 0.7: self.ditto_dir = random.choice(['left', 'right'])
                self.log(f"Starting Fluid Patrol: {self.ditto_dir.upper()}", "MAP")
                self.controller.key_down(self.ditto_dir)
                patrol_start = time.time(); encounter_found = False
                while (time.time() - patrol_start) < patrol_duration:
                    if not self.running or self.is_ui_present(self.observer.capture_frame()):
                        encounter_found = True; break
                    time.sleep(0.05)
                self.controller.key_up(self.ditto_dir)
                if not encounter_found: continue
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
            shiny_found = False; is_horde_detected = False; is_target = False; target_name = ""
            if mode == "ditto":
                hunter_name = self.config.get("hunter_pokemon_name", "Magikarp").lower()
                for attempt in range(max(1, ditto_ocr_retries)):
                    frame_battle = self.observer.capture_frame()
                    r_single = self.config.get("slot_single")
                    if not r_single: r_single = list(self.config.get("slots", {}).values())[0]
                    res = self.recognizer.analyze_slot(frame_battle[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']])
                    if res['is_shiny']: shiny_found = True; target_name = res['name']; break
                    if any(x in res['name'].lower() for x in ["ditto", "itto", "ditt", "ito"]): is_target = True; target_name = "Ditto"; break
                    if hunter_name in res['name'].lower() and len(res['name']) > 2: is_target = True; target_name = hunter_name; break
                    time.sleep(0.8)
            else:
                for attempt in range(ocr_retries_config):
                    frame_battle = self.observer.capture_frame()
                    total_id = 0; slots = self.config.get("slots", {})
                    for s_id, r in slots.items():
                        res = self.recognizer.analyze_slot(frame_battle[r['y1']:r['y2'], r['x1']:r['x2']])
                        if res['name']: total_id += 1; self.log_callback(f"   [#] {s_id.upper()}: {res['name']}")
                        if res['is_shiny']: shiny_found = True; target_name = res['name']; break
                    if total_id >= 3: is_horde_detected = True
                    if not shiny_found and mode == "single" and not is_horde_detected:
                        r_single = self.config.get("slot_single")
                        if r_single:
                            res = self.recognizer.analyze_slot(frame_battle[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']])
                            if res['name']: total_id += 1; self.log_callback(f"   [#] SINGLE: {res['name']}")
                            if res['is_shiny']: shiny_found = True; target_name = res['name']
                    if shiny_found or total_id > 0: break
                    time.sleep(1)

            if shiny_found:
                self.log_callback("\n✨✨✨ SHINY DETECTED! ✨✨✨\n")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.send_discord_alert("BATTLE", f"SHINY {target_name}!", "shiny_detected.png")
                if is_horde_detected: self.log("SHINY IN HORDE! Manual capture required.", "FATAL"); self.running = False; break
                else: is_target = True

            if is_target:
                is_soaked = False; has_swiped = False; turn_count = 1; slots_needing_leppa = set(); needs_potion = False
                while self.running:
                    frame_battle = self.observer.capture_frame()
                    if not self.is_ui_present(frame_battle) or not self.is_menu_present(frame_battle):
                        m = self.check_capture_success(frame_battle)
                        if m == "SUCCESS": break
                        time.sleep(3.0)
                        if not self.is_ui_present(self.observer.capture_frame()): break
                        continue
                    asleep = self.is_asleep(frame_battle); low_hp = self.is_hp_low(frame_battle) or has_swiped
                    if turn_count % 3 == 0 and self.read_hunter_hp(frame_battle): needs_potion = True
                    self.log_callback(f"  [ TURN {turn_count} ] HP:{'[LOW]' if low_hp else '[HI]'} ST:{'[SLP]' if asleep else '[AWK]'}")
                    mv_slot = None; mv_name = ""
                    if not has_swiped: mv_slot = self.config.get("ditto_key_attack", "2"); mv_name = "Swipe"
                    elif not is_soaked: mv_slot = self.config.get("ditto_key_soak", "4"); mv_name = "Soak"
                    elif not asleep: mv_slot = self.config.get("ditto_key_sleep", "1"); mv_name = "Sleep"
                    
                    if mv_slot:
                        self.controller.open_fight_menu(); time.sleep(0.6)
                        _, needs_res = self.read_pp(self.observer.capture_frame(), mv_slot, mv_name)
                        if needs_res: slots_needing_leppa.add((mv_slot, True))
                        self.controller.navigate_and_confirm_move(mv_slot)
                        if mv_name == "Swipe": has_swiped = True
                        if mv_name == "Soak": is_soaked = True
                        time.sleep(4.5)
                    else:
                        self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                        found_res = False
                        for _ in range(40): 
                            fm = self.observer.capture_frame()
                            res_m = self.check_capture_success(fm)
                            if res_m == "SUCCESS": found_res = True; break
                            elif res_m == "FAILURE": break
                            if not self.is_ui_present(fm): break
                            time.sleep(0.2)
                        if found_res: break
                    turn_count += 1
                self.encounters += 1; self.save_progress()
                self.log("Final cleanup...", "ACTION"); 
                for _ in range(6): self.controller._press('x'); time.sleep(0.6)
                if slots_needing_leppa or needs_potion:
                    time.sleep(2.0); self.log("Restoring HP/PP...", "ACTION")
                    if needs_potion: self.controller.use_potion_sequence(self.config.get("ditto_key_potion", "6"), full_heal=True); time.sleep(1.0)
                    l_key = self.config.get("ditto_key_leppa", "4")
                    for s_info in slots_needing_leppa: self.controller.use_leppa_sequence_single(l_key, s_info[0], full_restore=s_info[1])
                continue 

            escape_success = False
            for attempt in range(3):
                if not self.is_ui_present(self.observer.capture_frame()): escape_success = True; break
                self.controller.run_away()
                map_stable = 0
                for _ in range(15): 
                    time.sleep(0.15); 
                    if not self.is_ui_present(self.observer.capture_frame()): map_stable += 1
                    else: map_stable = 0
                    if map_stable >= 2: escape_success = True; break
                if escape_success: break
            if escape_success:
                self.encounters += 1; self.save_progress(); self.log_callback(f"  📊 TOTAL ENCOUNTERS: [ {self.encounters} ]")

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
