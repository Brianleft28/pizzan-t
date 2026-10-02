import time
import cv2
import random
from src.modes.base import HuntingMode

class DittoMode(HuntingMode):
    def __init__(self, bot):
        super().__init__(bot)
        self.direction = random.choice(['left', 'right'])
        self.walk_stamina = random.uniform(0.8, 1.2)
        self.monitoring_active = False

    def execute(self, frame):
        # 1. Observador Universal: Si no hay batalla, patrullar
        if not self.bot.check_any_name_visible(frame) and not self.bot.is_menu_ready(frame):
            base_t = float(self.config.get("ditto_patrol_time", 2.5))
            self.log(f"━━━━━ 🌍 PATROL ({self.direction.upper()}, {base_t:.1f}s) ━━━━━", "PHASE")
            self._human_patrol(self.direction, base_t, self.walk_stamina)
            
            # Post-patrulla logic
            self.walk_stamina = random.uniform(0.8, 1.2)
            if random.random() > 0.65:
                self.direction = 'left' if self.direction == 'right' else 'right'
            return

        if not self.bot.is_menu_ready(frame):
            if not self._wait_for_menu(): return

        # Escaneo Universal (resetea el timer de actividad automáticamente)
        f_bat = self.observer.capture_frame()
        shiny_found, target_name, all_names, slot_id = self.bot.scan_all_potential_targets(f_bat)
        
        # Log compacto del scan
        names_str = ", ".join([n.upper() for n in all_names]) if all_names else "NONE"
        self.log(f"Scan: {len(all_names)} target(s) → {names_str}", "BATTLE")

        is_target = False
        is_shiny = False
        if shiny_found:
            self.log(f"━━━━━ ✨ SHINY DETECTED! ━━━━━", "PHASE")
            self.log(f"✨ SHINY: {target_name.upper()} ✨", "SUCCESS")
            cv2.imwrite("shiny_detected.png", f_bat)
            self.bot.send_discord_alert("SINGLE/DITTO", f"SHINY {target_name}!", "shiny_detected.png")
            is_target = True
            is_shiny = True
        elif target_name and any(x in target_name.lower() for x in ["ditto", "itto", "ditt", "ito"]):
            is_target = True
            target_name = "Ditto"
            self.log(f"━━━━━ 🎯 DITTO DETECTED! ━━━━━", "PHASE")

        if not is_target:
            self.controller.run_away()
            self._wait_for_map()
            self.bot.encounters += 1
            self.bot.session_encounters += 1
            self.log(f"💨 Not Ditto ({target_name}). Escaped. [Enc #{self.bot.encounters} | Session: {self.bot.session_encounters}]", "ACTION")
            return

        self._capture_sequence(target_name, is_shiny=is_shiny)
        self.bot.session_dittos += 1
        self.bot.session_encounters += 1

    def _wait_for_map(self):
        esc_start = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if time.time() - esc_start > 5.0: break
            time.sleep(0.5)
        time.sleep(1.5)
