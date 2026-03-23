import pydirectinput
import time
import random

class PokéController:
    def __init__(self, config, log_callback=None):
        self.config_raw = config
        self.controls = config.get("controls", {})
        self.log_callback = log_callback
        self.variance = float(self.controls.get("human_variance", 0.2))
        # Desactivamos el pause de pydirectinput para manejarlo nosotros
        pydirectinput.PAUSE = 0.0

    def log(self, msg):
        if self.log_callback:
            # Clean and stylish terminal prefix
            self.log_callback(f"   [🎮] {msg}")

    def _human_wait(self, min_s, max_s):
        time.sleep(random.uniform(min_s, max_s))

    def _press(self, key, duration=None):
        """Presses a key with logs and precise timing"""
        # We don't log every single key press to avoid cluttering the ASCII art
        pydirectinput.keyDown(key)
        if duration:
            time.sleep(duration)
        else:
            time.sleep(random.uniform(0.12, 0.22))
        pydirectinput.keyUp(key)
        time.sleep(random.uniform(0.25, 0.45))

    def use_sweet_scent(self):
        key = self.controls.get("sweet_scent_key", "3")
        self._human_wait(0.5, 1.0)
        self.log(f"ACTIVATE: Sweet Scent (Key {key})")
        self._press(key)

    def search_movement(self):
        """High-speed humanoid movement to trigger encounters (Fast Step Zig-Zag)"""
        direction = random.choice(['left', 'right'])
        opposite = 'right' if direction == 'left' else 'left'
        
        steps = random.randint(2, 4)
        for i in range(steps):
            current_dir = direction if i < (steps // 2) else opposite
            duration = random.uniform(0.18, 0.28) 
            self._press(current_dir, duration=duration)
            time.sleep(random.uniform(0.02, 0.05))

    def run_away(self):
        """Navigates to the 'RUN' button with detailed logs"""
        path_id = random.randint(0, 3)
        self.log(f"ESCAPE PROTOCOL: Route {path_id}")
        
        # 1. Reset menu
        self._press('x')
        self._press('up')
        self._press('left')

        # 2. Routes
        if path_id == 0: # Direct
            self._press('right')
            self._press('down')
        elif path_id == 1: # Inverse
            self._press('down')
            self._press('right')
        elif path_id == 2: # Redundant
            self._press('right')
            self._press('down')
            self._press('down')
            self._press('down')
        else: # Doubt
            self._press('down')
            self._press('right')
            self._press('right')
            self._press('right')
            
        self.log("CONFIRM: Running away (Z)")
        self._press('z')
        
        if random.random() > 0.6:
            self._press('x')
