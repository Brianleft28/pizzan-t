import time
import cv2
from src.modes.base import HuntingMode

class HordeMode(HuntingMode):
    def __init__(self, bot):
        super().__init__(bot)

    def execute(self, frame):
        # 1. Mapa
        if not self.bot.is_menu_ready(frame) and not self.bot.check_any_name_visible(frame):
            self.log("Using Sweet Scent...", "ACTION")
            self.controller.use_sweet_scent()
            time.sleep(5.0)
            return

        # 2. Batalla
        if not self.bot.is_menu_ready(frame):
            self.log("Waiting for battle menu...", "BRAIN")
            if not self._wait_for_menu(): return

        # 3. Escaneo DESCRIPTIVO (MANDATO 2)
        f_bat = self.observer.capture_frame()
        shiny_found = False; target_name = "Unknown"
        
        self.log("SCANNIG HORDE SLOTS...", "BATTLE")
        h_slots = self.config.get("slots", {})
        for s_id, r in h_slots.items():
            res = self.bot.get_slot_data(f_bat, r)
            name = res['name'] if res['name'] else "Empty/Unknown"
            # LOG OBLIGATORIO DE CADA SLOT
            self.log(f"Detected Slot {s_id[-1]}: {name}", "BATTLE")
            
            if res['is_shiny']:
                shiny_found = True; target_name = name

        if shiny_found:
            self.log(f"SHINY DETECTED: {target_name.upper()}", "SUCCESS")
            cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
            self.bot.send_discord_alert("HORDE", f"SHINY {target_name}!", "shiny_detected.png")
            self.log("SHINY IN HORDE! STOPPING...", "FATAL")
            self.bot.running = False; return

        # 4. Escape
        self.log("Not shiny. Escaping...", "ACTION")
        self.controller.run_away()
        
        start_esc = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if (time.time() - start_esc) > 5.0: break
            time.sleep(0.5)
        
        self.bot.encounters += 5 # En hordas sumamos de a 5
        self.bot.save_progress()
        time.sleep(1.5)
