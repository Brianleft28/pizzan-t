import time
import random
from datetime import datetime, timedelta

class HuntingMode:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.observer = bot.observer
        self.recognizer = bot.recognizer
        self.controller = bot.controller
        self.log_callback = bot.log_callback

    def log(self, message, category="INFO"):
        timer = self.bot.get_elapsed_time()
        self.log_callback(f"[{timer}] [{category}] {message}")

    def execute(self, frame):
        """Método principal que debe ser implementado por cada modo"""
        raise NotImplementedError("Cada modo debe implementar su propio método execute")

    def _human_patrol(self, direction, base_time, walk_stamina):
        """MANDATO 2: Caminata que se corta instantáneamente al ver nombres arriba."""
        duration = (base_time * walk_stamina) * random.uniform(0.6, 1.4)
        self.log(f"Patrol: {direction.upper()} ({duration:.1f}s)", "MAP")
        
        self.controller.key_down(direction)
        start_walk = time.time()
        last_ocr_check = 0  # Temporizador de control
        
        while (time.time() - start_walk) < duration:
            if not self.bot.running: break
            
            # OPTIMIZACIÓN: Solo hacer OCR pesado 1 vez por segundo durante la caminata
            current_time = time.time()
            if current_time - last_ocr_check > 0.8:
                if self.bot.check_any_name_visible(self.observer.capture_frame()):
                    self.log("HUD Detected! Stopping patrol.", "BRAIN")
                    break
                last_ocr_check = current_time
                
            time.sleep(0.05)
            
        self.controller.key_up(direction)
        time.sleep(random.uniform(0.1, 0.3)) # Micro-pausa humana

    def _wait_for_menu(self, timeout=30):
        """Utilidad común para esperar a que el menú de batalla esté listo"""
        start = time.time()
        while (time.time() - start) < timeout:
            if not self.bot.running: return False
            if self.bot.is_menu_ready(self.observer.capture_frame()):
                return True
            time.sleep(0.2)
        return False

    def _capture_sequence(self, target_name, is_shiny=False):
        self.log(f"━━━━━━━━━━ 🎯 CAPTURE: {target_name.upper()} ━━━━━━━━━━", "PHASE")
        if is_shiny:
            self.log(f"✨ ¡SHINY CONFIRMADO! Activando alarma...", "SUCCESS")
            self.bot.play_shiny_alarm()
            
        turn = 1
        swiped = False
        leppas = set()
        captured = False

        while self.bot.running:
            self.bot.reset_activity_timer() 
            if not self._wait_for_menu(): break
            
            f_act = self.observer.capture_frame()
            is_slp = self.bot.is_asleep(f_act)
            is_low, hp_pct = self.bot.is_hp_low(f_act)
            
            # Decidir acción ANTES de loguear
            mv_s = None
            mv_n = ""
            action_desc = ""
            
            if turn == 1:
                mv_s = self.config.get("ditto_key_attack", "2")
                mv_n = self.config.get("ditto_name_attack", "Swipe")
                action_desc = f"⚔️ {mv_n} (Key {mv_s})"
            elif not is_slp:
                mv_s = self.config.get("ditto_key_sleep", "1")
                mv_n = self.config.get("ditto_name_sleep", "Sleep")
                action_desc = f"💤 {mv_n} (Key {mv_s})"
            else:
                mv_n = "Ball"
                action_desc = f"🟢 Throwing Ball"

            # Log estructurado del turno
            hp_status = f"LOW ({hp_pct:.0%})" if (is_low or swiped) else f"FULL ({hp_pct:.0%})"
            slp_status = "💤 SLP" if is_slp else "👁️ AWK"
            self.log(f"[T-{turn:02d}] HP: {hp_status} | {slp_status} | → {action_desc}", "BATTLE")

            if mv_s:
                self.controller.open_fight_menu()
                time.sleep(0.6)
                pp_curr, nr = self.bot.read_pp(mv_s, mv_n)
                
                if nr: 
                    leppas.add((mv_s, True))
                    self.log(f"[💊] PP for {mv_n} is {pp_curr}. Adding to restoration queue.", "HEAL")

                if pp_curr == 0:
                    self.log(f"⚠️ {mv_n} has 0 PP! Switching to Ball.", "WARN")
                    mv_s = None

                if mv_s:
                    self.controller.navigate_and_confirm_move(mv_s)
                    if mv_n == self.config.get("ditto_name_attack", "Swipe"):
                        swiped = True
                    time.sleep(2.0)
                    while self.bot.is_menu_ready(self.observer.capture_frame()) and self.bot.running:
                        time.sleep(0.5)
            
            if not mv_s:
                self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                if self._check_capture_result():
                    captured = True
                    break
            
            turn += 1

        # Resultado real de la captura
        self.bot.encounters += 1
        self.bot.save_progress()
        
        if captured:
            self.log(f"✅ CAPTURE CONFIRMED: {target_name.upper()} in {turn} turns!", "SUCCESS")
        else:
            self.log(f"❌ CAPTURE ENDED: {target_name.upper()} — {turn} turns (timeout/stop)", "WARN")
        
        if is_shiny and captured:
            self.log("✨ 🎉 ¡BRUTAL! ¡HAS ATRAPADO UN SHINY! ¡FELICIDADES! 🎉 ✨", "SUCCESS")
            self.bot.stop_shiny_alarm()

        if leppas and self.config.get("auto_heal_pp", True):
            self.log("━━━━━━━━━━ 💊 HEALING ━━━━━━━━━━", "PHASE")
            leppa_wait = float(self.config.get("timing_leppa_wait", 1.5))
            self.log(f"⏳ Waiting {leppa_wait}s for map to load before Leppa...", "HEAL")
            time.sleep(leppa_wait)
            self.bot.reset_activity_timer()
            self.log(f"Restoring {len(leppas)} move(s) from PP queue...", "HEAL")
            for slot_data in list(leppas):
                self.controller.use_leppa_sequence_single(self.config.get("ditto_key_leppa", "4"), slot_data[0], slot_data[1])
                time.sleep(1.0)

        # Limpieza final por si quedó algún diálogo abierto
        time.sleep(0.5)
        self.controller._press('x')
        self.controller._press('z')
        time.sleep(0.3)
        self.controller._press('x')
        self.log(f"━━━━━━━━━━ END CAPTURE ━━━━━━━━━━", "PHASE")

    def _check_capture_result(self):
        """
        Espera el resultado de la Pokébola con spamming activo de la interfaz para evitar UI overlap.
        """
        ball_wait   = float(self.config.get("timing_ball_wait", 0.5))
        settle_time = float(self.config.get("timing_capture_settle", 2.5))

        self.log(f"⏳ Waiting {ball_wait}s for ball animation...", "DEBUG")
        time.sleep(ball_wait)

        for _ in range(60):
            if not self.bot.running:
                return False
                
            # ACTIVE POLLING: Destruimos ventanas emergentes de stats para que el OCR pueda ver el "CAUGHT"
            self.controller._press('left', duration=0.02)
            self.controller._press('x', duration=0.02)
            self.controller._press('right', duration=0.02)
            self.controller._press('x', duration=0.02)
            
            # Recién ahora tomamos captura, con el texto presumiblemente limpio
            fb = self.observer.capture_frame()
            m = self.bot.check_msg_area(fb)

            if m == "SUCCESS":
                self.log("🎉 Message read: CAUGHT!", "SUCCESS")
                time.sleep(settle_time)
                # Cerrar diálogos adicionales
                for _ in range(8):
                    self.controller._press('z', duration=0.05)
                    self.controller._press('x', duration=0.05)
                    time.sleep(0.3)
                return True

            if m == "FAILURE":
                self.log("💨 Ball broke free — retrying next turn.", "WARN")
                time.sleep(1.5)
                return False

            if self.bot.is_menu_ready(fb):
                return False

            time.sleep(0.1) # Agilizamos el poll

        # TIMEOUT FIX: Si el loop terminó y no volvió el menú de batalla, deducimos captura
        self.log("⏱️ No battle menu returned. Assuming CAUGHT due to UI overlap!", "SUCCESS")
        return True

