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
            # CORRECCIÓN: Pasar los argumentos requeridos
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
        
        self.log(f"BATTLEFIELD SCAN: {len(all_names)} targets.", "BATTLE")
        for i, name in enumerate(all_names):
            self.log(f"Target {i+1}: {name.upper()}", "BATTLE")

        is_target = False
        if shiny_found:
            self.log(f"✨ SHINY DETECTADO: {target_name.upper()} ✨", "SUCCESS")
            cv2.imwrite("shiny_detected.png", f_bat)
            self.bot.send_discord_alert("SINGLE", f"SHINY {target_name}!", "shiny_detected.png")
            is_target = True
        elif target_name and any(x in target_name.lower() for x in ["ditto", "itto", "ditt", "ito"]):
            is_target = True
            target_name = "Ditto"

        if not is_target:
            self.log(f"Not target ({target_name}). Escaping...", "ACTION")
            self.controller.run_away()
            self._wait_for_map()
            self.bot.encounters += 1
            self.bot.session_encounters += 1
            return

        self._capture_sequence(target_name)

    def _capture_sequence(self, target_name):
        self.log(f"INITIATING CAPTURE: {target_name.upper()}", "ACTION")
        self.monitoring_active = False
        turn = 1
        swiped = False; needs_pot = False; leppas = set()

        while self.bot.running:
            self.bot.reset_activity_timer() 
            if not self._wait_for_menu(): break
            
            f_act = self.observer.capture_frame()
            is_slp = self.bot.is_asleep(f_act)
            is_low, _ = self.bot.is_hp_low(f_act)
            
            pot_n, h_hp, _ = self.bot.read_hunter_hp()
            if pot_n: 
                needs_pot = True
                self.log(f"Hunter HP Critical ({h_hp}). Adding Potion to queue.", "HEAL")
            
            h_status = "CRITICAL" if pot_n else "OK"
            self.log(f"[T-{turn:02d}] Enemy: {'LOW' if (is_low or swiped) else 'HIGH'} | Status: {'SLP' if is_slp else 'AWK'} | Hunter: {h_hp} ({h_status})", "DEBUG")

            mv_s = None; mv_n = ""
            if turn == 1:
                mv_s = self.config.get("ditto_key_attack", "2"); mv_n = self.config.get("ditto_name_attack", "Swipe")
            elif not is_slp:
                mv_s = self.config.get("ditto_key_sleep", "1"); mv_n = self.config.get("ditto_name_sleep", "Sleep")
                if not self.monitoring_active:
                    self.log("Status Monitor Activated: Target will be kept asleep.", "DEBUG")
                    self.monitoring_active = True
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
        self.bot.session_encounters += 1
        self.bot.session_dittos += 1
        self.bot.save_progress()
        
        self.log(f"CAPTURE SUCCESSFUL: {target_name.upper()} (Session: {self.bot.session_dittos})", "SUCCESS")
        
        if needs_pot and self.config.get("auto_heal_hp", True):
            self.bot.reset_activity_timer()
            self.log("Restoring Hunter HP...", "HEAL")
            self.controller.use_potion_sequence(self.config.get("ditto_key_potion", "6"), True)

        if leppas and self.config.get("auto_heal_pp", True):
            self.bot.reset_activity_timer()
            self.log("Restoring PPs from queue...", "HEAL")
            for s in leppas:
                self.controller.use_leppa_sequence_single(self.config.get("ditto_key_leppa", "4"), s[0], s[1])

        time.sleep(2.0); self.controller._press('x'); time.sleep(0.4); self.controller._press('x')

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

    def _wait_for_map(self):
        esc_start = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if time.time() - esc_start > 5.0: break
            time.sleep(0.5)
        time.sleep(1.5)
