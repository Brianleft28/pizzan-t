import time
import cv2
import random
from src.modes.base import HuntingMode

class SingleMode(HuntingMode):
    def __init__(self, bot):
        super().__init__(bot)
        self.direction = random.choice(['left', 'right'])
        self.walk_stamina = random.uniform(0.8, 1.2)

    def execute(self, frame):
        # 1. Observador Universal: Si no hay batalla, patrullar
        if not self.bot.check_any_name_visible(frame) and not self.bot.is_menu_ready(frame):
            # Usamos el tiempo de patrulla de la UI (compartido con Ditto)
            base_t = float(self.config.get("ditto_patrol_time", 2.5))
            self._human_patrol(self.direction, base_t, self.walk_stamina)
            
            # Post-patrulla
            self.walk_stamina = random.uniform(0.8, 1.2)
            if random.random() > 0.65:
                self.direction = 'left' if self.direction == 'right' else 'right'
            return

        # 2. Batalla Detectada
        if not self.bot.is_menu_ready(frame):
            if not self._wait_for_menu(): return

        # 3. ESCANEO UNIVERSAL (MANDATO 2)
        f_bat = self.observer.capture_frame()
        shiny_found, target_name, all_names, slot_id = self.bot.scan_all_potential_targets(f_bat)
        
        self.log(f"BATTLEFIELD SCAN: {len(all_names)} targets.", "BATTLE")
        for i, name in enumerate(all_names):
            self.log(f"Target {i+1}: {name.upper()}", "BATTLE")

        if shiny_found:
            self.log(f"✨ SHINY DETECTADO: {target_name.upper()} ✨", "SUCCESS")
            cv2.imwrite("shiny_detected.png", f_bat)
            self.bot.send_discord_alert("SINGLE", f"SHINY {target_name}!", "shiny_detected.png")
            self.log("SHINY FOUND! STOPPING...", "FATAL")
            self.bot.running = False
            return

        # 4. Escape si no es shiny
        self.log(f"Not shiny ({target_name}). Escaping...", "ACTION")
        self.controller.run_away()
        self._wait_for_map()
        self.bot.encounters += 1
        self.bot.save_progress()
        time.sleep(1.5)

    def _wait_for_map(self):
        esc_start = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if time.time() - esc_start > 5.0: break
            time.sleep(0.5)
        time.sleep(1.0)
