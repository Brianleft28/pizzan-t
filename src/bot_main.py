import cv2
import time
import json
import os
import requests
import random
import numpy as np
import re
import winsound
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
        self.last_activity_time = time.time()
        self._alarm_active = False
        
        self.logger = PokéLogger(log_widget)
        self.log_callback = self.logger.log
        
        try:
            self.config = self.load_config()
            self.observer = PokéObserver()
            self.recognizer = PokéRecognizer()
            self.controller = PokéController(self.config, log_callback=self.log_callback)
            
            self.encounters = int(self.config.get("total_encounters", 0))
            self.session_encounters = 0
            self.session_dittos = 0
            
            self.mode_instance = self._initialize_mode()
            
            self.logger.log("---------------------------------------")
            self.logger.log("  THE HUMANOID HUNTER v6.9 - SENTINEL ", "SUCCESS")
            self.logger.log("---------------------------------------")
        except Exception as e: 
            self.logger.log(f"Bot initialization failed: {e}", "FATAL")

    def reset_activity_timer(self):
        self.last_activity_time = time.time()

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
        return self.logger.get_elapsed()

    def log(self, message, category="INFO"):
        self.logger.log(message, category)

    def is_menu_ready(self, frame):
        r = self.config.get("button_run")
        if not r or frame is None: return False
        crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
        res = self.recognizer.reader.readtext(crop)
        txt = " ".join([rm[1].lower() for rm in res])
        keywords = ["run", "huir", "huida", "fight", "luch", "bag", "moch", "pkmn", "poke", "ata", "batalla", "combate", "escapar"]
        if any(k in txt for k in keywords):
            self.reset_activity_timer() # Ver el menú es actividad
            return True
        return False

    def get_slot_data(self, frame, region):
        crop = frame[region['y1']:region['y2'], region['x1']:region['x2']]
        return self.recognizer.analyze_slot(crop)

    def scan_all_potential_targets(self, frame):
        all_results = []
        shiny_detected = False
        target_name = None
        shiny_slot = None

        h_size = self.config.get("horde_size", 5)
        h_slots = self.config.get(f"slots_{h_size}", self.config.get("slots", {}))

        for s_id, r in h_slots.items():
            res = self.get_slot_data(frame, r)
            if res['name'] and len(res['name']) > 2:
                all_results.append(res['name'])
                if res['is_shiny']:
                    shiny_detected = True; target_name = res['name']; shiny_slot = f"HORDE_{s_id[-1]}"

        r_s = self.config.get("slot_single")
        if r_s:
            res_s = self.get_slot_data(frame, r_s)
            if res_s['name'] and len(res_s['name']) > 2:
                all_results.append(res_s['name'])
                if res_s['is_shiny'] and not shiny_detected:
                    shiny_detected = True; target_name = res_s['name']; shiny_slot = "SINGLE"
                elif not target_name:
                    target_name = res_s['name']

        if all_results: self.reset_activity_timer() 
        return shiny_detected, target_name, all_results, shiny_slot

    def check_any_name_visible(self, frame):
        if frame is None: return False
        h_size = self.config.get("horde_size", 5)
        h_slots = self.config.get(f"slots_{h_size}", self.config.get("slots", {}))
        
        for s_id, r in h_slots.items():
            res = self.get_slot_data(frame, r)
            if res['name'] and len(res['name']) > 2: 
                self.reset_activity_timer()
                return True
        r_s = self.config.get("slot_single")
        if r_s:
            res_s = self.get_slot_data(frame, r_s)
            if res_s['name'] and len(res_s['name']) > 2: 
                self.reset_activity_timer()
                return True
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

    def read_hunter_hp(self, frame_dummy=None):
        r = self.config.get("hunter_hp_region")
        if not r: return False, "??/??", 0
        for attempt in range(4):
            frame = self.observer.capture_frame()
            crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            res = self.recognizer.reader.readtext(upscaled)
            txt = "".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1').replace('S', '5')
            self.log(f"RAW HP OCR [Att {attempt+1}]: '{txt}'", "DEBUG")
            nums = re.findall(r'(\d+)', txt)
            if len(nums) >= 2:
                self.reset_activity_timer() # Éxito en lectura = actividad
                curr, total = int(nums[0]), int(nums[1])
                return (total - curr >= 60), f"{curr}/{total}", (total - curr)
            time.sleep(0.3)
        return False, "??/??", 0

    def read_pp(self, slot_idx, move_name="Move"):
        pp_slots = self.config.get("pp_slots", {})
        slot_key = f"slot_{slot_idx}"
        if slot_key not in pp_slots: return 99, False
        r = pp_slots[slot_key]
        for attempt in range(4):
            frame = self.observer.capture_frame()
            crop = frame[r['y1']:r['y2'], r['x1']:r['x2']]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            res = self.recognizer.reader.readtext(upscaled)
            txt = "".join([rm[1] for rm in res]).upper().replace('O', '0').replace('I', '1').replace('S', '5').replace('B', '8')
            self.log(f"RAW PP OCR [Att {attempt+1}]: '{txt}'", "DEBUG")
            nums = re.findall(r'(\d+)', txt)
            if len(nums) >= 2:
                self.reset_activity_timer() # Éxito en lectura = actividad
                curr, total = int(nums[0]), int(nums[1])
                # CAMBIO: Solo restaurar si queda 0 o 1 PP para no desperdiciar Zanamas
                return curr, (curr <= 1)
            time.sleep(0.3)
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
        if not url:
            self.log("Discord Webhook URL not configured.", "WARN")
            return
            
        self.log(f"Sending Discord alert: {category} - {message}...", "INFO")
        try:
            with open(img_path, "rb") as f:
                # Usamos una estructura más robusta para Discord
                payload = {"content": f"🚨 **{category} DETECTED** 🚨\n> {message}\n> Total Encounters: {self.encounters}"}
                files = {"file": (img_path, f, "image/png")}
                response = requests.post(url, data=payload, files=files, timeout=10)
                
                if response.status_code in [200, 204]:
                    self.log("✅ Discord alert sent successfully!", "SUCCESS")
                else:
                    self.log(f"❌ Discord error: {response.status_code} - {response.text}", "FATAL")
        except Exception as e:
            self.log(f"❌ Failed to send Discord alert: {e}", "FATAL")

    def panic_stop(self):
        """MANDATO DE SEGURIDAD: Detiene todo para proteger un Shiny"""
        self.running = False
        self.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "FATAL")
        self.log("!!!   PANIC STOP: SHINY DETECTED    !!!", "FATAL")
        self.log("!!!    MANUAL INTERVENTION REQD     !!!", "FATAL")
        self.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "FATAL")
        self.play_shiny_alarm()

    def play_shiny_alarm(self):
        if self._alarm_active: return
        self._alarm_active = True
        
        def _alarm_loop():
            path = os.path.join("assets", "shiny_alarm.wav")
            while self._alarm_active:
                if not os.path.exists(path):
                    self.log(f"⚠️ Alarm sound not found at {path}. Use .wav format.", "WARN")
                    for _ in range(10): 
                        if not self._alarm_active: break
                        winsound.Beep(1000, 500)
                    break
                
                self.log("📢 Playing SHINY ALARM (18s loop)...", "INFO")
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                
                start_wait = time.time()
                while time.time() - start_wait < 18:
                    if not self._alarm_active: 
                        winsound.PlaySound(None, winsound.SND_PURGE)
                        return
                    time.sleep(0.1)
        
        Thread(target=_alarm_loop, daemon=True).start()

    def stop_shiny_alarm(self):
        self._alarm_active = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.log("🔇 Alarm stopped.", "INFO")

    def check_guardian(self, frame):
        """MANDATO 3: El Guardián es más cauteloso"""
        if time.time() - self.last_activity_time > 45: # Aumentado a 45s para dar margen a capturas
            self.log("GUARDIAN: System idle for 45s. Checking state...", "WARN")
            
            # Solo actuamos si el HUD parece trabado
            if self.check_any_name_visible(frame) or self.is_menu_ready(frame):
                self.log("GUARDIAN: HUD detected but no progress. Verifying for 9s...", "WARN")
                st = time.time()
                while (time.time() - st) < 9.0:
                    if not self.running: return
                    time.sleep(1.0)
                
                # Si tras 9s el timer no se reseteó (nadie leyó nada exitoso), limpiamos
                if time.time() - self.last_activity_time > 50:
                    self.log("GUARDIAN: Recovery sequence initiated.", "FATAL")
                    self.controller._press('x')
                    time.sleep(0.5)
                    self.controller.run_away()
            
            self.reset_activity_timer()

    def loop(self):
        self.start_time = datetime.now()
        self.logger.clear_start_time()
        self.reset_activity_timer()
        while self.running:
            try:
                frame = self.observer.capture_frame()
                if frame is None: continue
                self.check_guardian(frame)
                self.mode_instance.execute(frame)
                time.sleep(0.1)
            except Exception as e:
                self.log(f"LOOP ERROR: {e}", "FATAL")
                time.sleep(1.0)

    def start(self):
        self.running = True; self.thread = Thread(target=self.loop, daemon=True); self.thread.start()

    def stop(self):
        self.running = False; self.save_progress()
