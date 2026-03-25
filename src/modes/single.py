import time
import cv2
from src.modes.base import HuntingMode

class SingleMode(HuntingMode):
    def __init__(self, bot):
        super().__init__(bot)

    def execute(self, frame):
        # 1. Si no hay menú ni nombres visibles, estamos en el mapa
        if not self.bot.is_menu_ready(frame) and not self.bot.check_any_name_visible(frame):
            self.log("Searching in grass...", "ACTION")
            self.controller.search_movement() # Usa movimiento aleatorio
            return

        # 2. Batalla Detectada
        if not self.bot.is_menu_ready(frame):
            if not self._wait_for_menu(): return

        # 3. Escaneo
        f_bat = self.observer.capture_frame()
        r_s = self.config.get("slot_single")
        res_s = self.bot.get_slot_data(f_bat, r_s)

        if res_s['name']:
            self.log(f"Detected: {res_s['name']}", "BATTLE")
            if res_s['is_shiny']:
                self.bot.log_callback("\n✨✨✨ SHINY DETECTADO: " + res_s['name'].upper() + " ✨✨✨")
                cv2.imwrite("shiny_detected.png", self.observer.capture_frame())
                self.bot.send_discord_alert("BATTLE", f"SHINY {res_s['name']}!", "shiny_detected.png")
                self.log("SHINY FOUND! MANUAL REQUIRED.", "FATAL")
                self.bot.running = False
                return

        # 4. En modo Single, si no es shiny, escapamos
        self.log("Not shiny. Escaping...", "INFO")
        self.controller.run_away()
        
        # Esperar a que la pantalla se limpie
        start_esc = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if (time.time() - start_esc) > 5.0: break
            time.sleep(0.5)
        
        self.bot.encounters += 1
        self.bot.save_progress()
        time.sleep(1.5)
