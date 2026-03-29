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
        
        while (time.time() - start_walk) < duration:
            if not self.bot.running: break
            # Chequeo atómico: Si vemos cualquier nombre arriba, soltamos la tecla YA.
            if self.bot.check_any_name_visible(self.observer.capture_frame()):
                self.log("HUD Detected! Stopping patrol.", "BRAIN")
                break
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

    def _capture_sequence(self, target_name):
        self.log(f"INITIATING CAPTURE: {target_name.upper()}", "ACTION")
        turn = 1
        swiped = False; leppas = set()

        while self.bot.running:
            self.bot.reset_activity_timer() 
            if not self._wait_for_menu(): break
            
            f_act = self.observer.capture_frame()
            is_slp = self.bot.is_asleep(f_act)
            is_low, _ = self.bot.is_hp_low(f_act)
            
            self.log(f"[T-{turn:02d}] Enemy: {'LOW' if (is_low or swiped) else 'HIGH'} | Status: {'SLP' if is_slp else 'AWK'}", "DEBUG")

            mv_s = None; mv_n = ""
            if turn == 1:
                mv_s = self.config.get("ditto_key_attack", "2"); mv_n = self.config.get("ditto_name_attack", "Swipe")
            elif not is_slp:
                mv_s = self.config.get("ditto_key_sleep", "1"); mv_n = self.config.get("ditto_name_sleep", "Sleep")
            else:
                mv_n = "Ball"

            if mv_s:
                self.controller.open_fight_menu(); time.sleep(0.6)
                pp_curr, nr = self.bot.read_pp(mv_s, mv_n)
                self.log(f"Move: {mv_n} | PP Check: {pp_curr}", "DEBUG")
                if nr: 
                    leppas.add((mv_s, True))
                    self.log(f"PP for {mv_n} is {pp_curr}. Adding Leppa to queue.", "HEAL")
                
                self.controller.navigate_and_confirm_move(mv_s)
                if mv_n == self.config.get("ditto_name_attack", "Swipe"): swiped = True
                
                time.sleep(2.0)
                while self.bot.is_menu_ready(self.observer.capture_frame()) and self.bot.running: time.sleep(0.5)
            else:
                self.controller.use_ball(self.config.get("ditto_key_ball", "5"))
                if self._check_capture_result(): break
            
            turn += 1

        self.bot.encounters += 1
        self.bot.save_progress()
        self.log(f"CAPTURE SUCCESSFUL: {target_name.upper()}", "SUCCESS")
        
        if leppas and self.config.get("auto_heal_pp", True):
            self.bot.reset_activity_timer()
            self.log(f"Restoring {len(leppas)} moves from PP queue...", "HEAL")
            for slot_data in list(leppas):
                self.controller.use_leppa_sequence_single(self.config.get("ditto_key_leppa", "4"), slot_data[0], slot_data[1])
                time.sleep(1.0)

        time.sleep(1.0); self.controller._press('x'); time.sleep(0.4); self.controller._press('x')

    def _check_capture_result(self):
        for _ in range(60): 
            fb = self.observer.capture_frame()
            m = self.bot.check_msg_area(fb)
            if m == "SUCCESS": 
                self.log("CAPTURE CONFIRMED!", "SUCCESS")
                for _ in range(6): self.controller._press('x'); time.sleep(0.5)
                return True
            if self.bot.is_menu_ready(fb): return False
            time.sleep(0.2)
        return False
