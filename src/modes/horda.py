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
            if not self._wait_for_menu(): return

        # 3. ESCANEO UNIVERSAL (MANDATO 2)
        f_bat = self.observer.capture_frame()
        shiny_found, target_name, all_names, slot_id = self.bot.scan_all_potential_targets(f_bat)
        
        self.log(f"BATTLEFIELD SCAN: {len(all_names)} targets found.", "BATTLE")
        for i, name in enumerate(all_names):
            self.log(f"Target {i+1}: {name.upper()}", "BATTLE")

        if shiny_found:
            self.log(f"✨ SHINY DETECTADO: {target_name.upper()} ✨", "SUCCESS")
            cv2.imwrite("shiny_detected.png", f_bat)
            self.bot.send_discord_alert("HORDE", f"SHINY {target_name}!", "shiny_detected.png")
            self.bot.panic_stop()
            return

        # 4. Escape
        self.log("No shiny in battlefield. Escaping...", "ACTION")
        self.controller.run_away()
        self._wait_for_map()
        h_size = self.bot.config.get("horde_size", 5)
        self.bot.encounters += int(h_size)
        self.bot.save_progress()
        time.sleep(1.5)

    def _wait_for_map(self):
        esc_start = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if time.time() - esc_start > 5.0: break
            time.sleep(0.5)
        time.sleep(1.0)
