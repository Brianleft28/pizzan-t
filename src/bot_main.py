import cv2
import time
import json
import os
import requests
import random
import numpy as np
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
            self.last_horda_id = "" 
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
        """Detects HUD presence. Returns True if a horde or a single slot is detected."""
        mode = self.config.get("mode", "horda")
        slots = self.config.get("slots", {})
        
        # Check Horde Slots first
        horde_present_count = 0
        for s_id, r in slots.items():
            crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh) > 150: horde_present_count += 1
        
        if horde_present_count >= 3:
            return True
            
        if mode == "single":
            r_single = self.config.get("slot_single")
            if not r_single and slots: r_single = list(slots.values())[0]
            if r_single:
                crop = frame[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']]
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
                return cv2.countNonZero(thresh) > 150
                
        return False

    def is_menu_present(self, frame, debug=False):
        """Verifies if the 'Run' button menu is visible using OCR and Pixel check."""
        btn_run = self.config.get("button_run")
        if not btn_run: return False
        
        menu_zone = frame[btn_run['y1']:btn_run['y2'], btn_run['x1']:btn_run['x2']]
        gray = cv2.cvtColor(menu_zone, cv2.COLOR_BGR2GRAY)
        
        # Test 1: Pixel brightness
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        bright_pixels = cv2.countNonZero(thresh)
        
        # Test 2: OCR
        enhanced = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        results = self.recognizer.reader.readtext(enhanced)
        full_text = " ".join([res[1].lower() for res in results])
        
        if debug or (bright_pixels > 50):
            self.log(f"MENU CHECK -> Pixels: {bright_pixels} | Text: '{full_text}'", "DEBUG")

        keywords = ["huid", "huir", "run", "ida", "uid", "gui", "da", "hu"]
        if bright_pixels > 80 or any(k in full_text for k in keywords):
            return True
            
        return False

    def loop(self):
        mode = self.config.get("mode", "horda")
        ocr_retries_config = int(self.config.get("ocr_retries", 6))
        
        self.log_callback(f"\n╔══════════════════════════════════════════╗")
        self.log_callback(f"║  STARTING HUNT IN {mode.upper()} MODE   ║")
        self.log_callback(f"╚══════════════════════════════════════════╝\n")
        
        while self.running:
            frame = self.observer.capture_frame()
            if frame is None: continue

            # --- 1. STATE: MAP (Looking for Encounter) ---
            if not self.is_ui_present(frame):
                if mode == "horda":
                    self.log("Using Sweet Scent...", "MAP")
                    self.controller.use_sweet_scent()
                else:
                    self.log("Humanoid Wiggle Search...", "MAP")
                    while self.running:
                        self.controller.search_movement()
                        time.sleep(0.05)
                        if self.is_ui_present(self.observer.capture_frame()):
                            self.log("Encounter triggered!", "INFO")
                            break
                
                # Wait for stabilization
                encounter_confirmed = False
                for _ in range(60): 
                    time.sleep(0.2)
                    if self.is_ui_present(self.observer.capture_frame()):
                        encounter_confirmed = True
                        break
                if not encounter_confirmed: continue

            # --- 2. STATE: BATTLE (Waiting for Menu) ---
            self.log("Waiting for battle menu commands...", "BATTLE")
            menu_ready = False
            for i in range(50): 
                if self.is_menu_present(self.observer.capture_frame(), debug=(i % 10 == 0)):
                    menu_ready = True
                    break
                time.sleep(0.2)
            
            if not menu_ready:
                self.log("Menu not detected, forcing analysis...", "WARN")

            # --- 3. STATE: ANALYSIS ---
            self.log_callback("\n  ┌───────────────────────────────────┐")
            self.log_callback("  │         ANALYZING BATTLE           │")
            self.log_callback("  └───────────────────────────────────┘")
            
            time.sleep(0.5)
            shiny_found = False
            total_identified = 0
            is_horde_detected = False
            
            for attempt in range(ocr_retries_config):
                frame_battle = self.observer.capture_frame()
                total_identified = 0
                
                # Hybrid Strategy: Always check for Horde first
                slots = self.config.get("slots", {})
                present_horde_slots = 0
                for slot_id, r in slots.items():
                    res = self.recognizer.analyze_slot(frame_battle[r['y1']:r['y2'], r['x1']:r['x2']])
                    name = res['name'].strip()
                    if name:
                        total_identified += 1
                        self.log_callback(f"   [#] {slot_id.upper()}: {name}")
                        present_horde_slots += 1
                    if res['is_shiny']:
                        shiny_found = True
                        self.log(f"SHINY DETECTED IN HORDE SLOT {slot_id.upper()}!", "!!!")
                        break
                
                if present_horde_slots >= 3:
                    is_horde_detected = True

                # If no shiny in horde slots and we are in single mode, check single slot
                if not shiny_found and mode == "single" and not is_horde_detected:
                    r_single = self.config.get("slot_single")
                    if r_single:
                        res = self.recognizer.analyze_slot(frame_battle[r_single['y1']:r_single['y2'], r_single['x1']:r_single['x2']])
                        name = res['name'].strip()
                        if name:
                            total_identified += 1
                            self.log_callback(f"   [#] SINGLE SLOT: {name}")
                        if res['is_shiny']:
                            shiny_found = True
                            self.log("SHINY DETECTED IN SINGLE SLOT!", "!!!")

                if shiny_found or total_identified > 0:
                    break
                
                self.log(f"OCR attempt {attempt+1}/{ocr_retries_config} failed. Retrying...", "OCR")
                time.sleep(1)

            if shiny_found:
                self.log_callback("\n" + r"""
   ✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
   ✨      SHINY POKÉMON DETECTED!       ✨
   ✨       ALERT SENT TO DISCORD!       ✨
   ✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
                """ + "\n")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.send_discord_alert("BATTLE", "SHINY FOUND!", "shiny_detected.png")
                self.running = False
                break
            
            if total_identified == 0:
                self.log("OCR failure. Escaping for safety.", "WARN")

            # --- 4. STATE: ESCAPE ---
            escape_success = False
            for attempt in range(3):
                self.log(f"Checking Run menu (Try {attempt+1})...", "ESCAPE")
                ready_to_run = False
                for _ in range(15): 
                    if self.is_menu_present(self.observer.capture_frame()):
                        ready_to_run = True
                        break
                    time.sleep(0.2)
                
                if not ready_to_run:
                    self.log("Run button not found. Battle might be busy.", "WARN")
                
                self.log("Executing Escape maneuvers...", "ACTION")
                self.controller.run_away()
                
                # Verify return to map
                map_stable = 0
                for _ in range(40): 
                    time.sleep(0.2)
                    if not self.is_ui_present(self.observer.capture_frame()):
                        map_stable += 1
                    else:
                        map_stable = 0
                    
                    if map_stable >= 4: 
                        escape_success = True
                        break
                
                if escape_success: break
                self.log("Still in battle. Retrying escape...", "WARN")
            
            if not escape_success:
                self.log("Failed to exit battle. Emergency stop.", "FATAL")
                self.running = False
                break

            # --- 5. END OF CYCLE ---
            # Smart Counter: If we detected a horde (even in single mode), +5. Otherwise +1.
            inc = 5 if is_horde_detected else 1
            self.encounters += inc
            self.log_callback(f"\n  📊 TOTAL ENCOUNTERS: [ {self.encounters} ]")
            self.save_progress()
            self.log_callback(f"  -------------------------------------")

    def send_discord_alert(self, slot, name, img_path):
        url = self.config.get("discord_webhook")
        if not url: return
        content = f"🏆 SHINY FOUND! {name} in {slot} | Total: {self.encounters}"
        try:
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    requests.post(url, data={"content": content}, files={"file": f})
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
        self.running = False
        self.save_progress()
