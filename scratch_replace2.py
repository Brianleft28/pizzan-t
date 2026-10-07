import sys
import re

with open("src/modes/base.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the entire _check_capture_result function up to the next method or end of file
pattern = re.compile(r"    def _check_capture_result\(self\):.*?        return False.*?(?=    def |$)", re.DOTALL)

new_func = """    def _check_capture_result(self):
        \"\"\"
        Espera el resultado de la Pokebola basandose en el estado de la UI
        en lugar de leer texto, para evitar el cuelgue por OCR.
        \"\"\"
        ball_wait   = float(self.config.get("timing_ball_wait", 0.5))
        settle_time = float(self.config.get("timing_capture_settle", 2.5))
        spam_delay  = float(self.config.get("timing_capture_spam_delay", 0.3))

        self.log(f"? Waiting {ball_wait}s for ball animation...", "DEBUG")
        time.sleep(ball_wait)

        for _ in range(60):
            if not self.bot.running:
                return False
                
            # Presionamos 'x' para saltar pokedex o stats de nivel
            self.controller._press('x', duration=0.05)
            
            fb = self.observer.capture_frame()
            
            # 1. Si el menu de batalla vuelve a aparecer, la bola se rompio y es nuestro turno de nuevo.
            if self.bot.is_menu_ready(fb):
                self.log("? Ball broke free - retrying next turn.", "WARN")
                time.sleep(0.5)
                return False
                
            # 2. Si el nombre superior del enemigo desaparece de la pantalla, la batalla termino (Captura exitosa).
            if not self.bot.check_any_name_visible(fb):
                self.log("? Capture confirmed! Enemy name cleared from HUD.", "SUCCESS")
                time.sleep(settle_time)
                # Cerrar cualquier dialogo residual (Pokedex, stats)
                for _ in range(8):
                    self.controller._press('z', duration=0.05)
                    self.controller._press('x', duration=0.05)
                    time.sleep(0.3)
                return True

            # Esperar antes de la siguiente iteracion (la bola sigue girando)
            time.sleep(spam_delay)
            
        return False
"""

content = pattern.sub(new_func, content, count=1)

with open("src/modes/base.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
