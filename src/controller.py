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

    def key_down(self, key):
        """Holds a key down without releasing it"""
        pydirectinput.keyDown(key)

    def key_up(self, key):
        """Releases a held key"""
        pydirectinput.keyUp(key)

    def _press(self, key, duration=None):
        """Presses a key with precise timing and a mandatory human-like pause"""
        pydirectinput.keyDown(key)
        if duration:
            time.sleep(duration)
        else:
            time.sleep(random.uniform(0.12, 0.22))
        pydirectinput.keyUp(key)
        # Trailing sleep to avoid "robo-speed" in menus
        time.sleep(random.uniform(0.2, 0.35))

    def use_sweet_scent(self):
        key = self.controls.get("sweet_scent_key", "3")
        self._human_wait(0.5, 1.0)
        self.log(f"ACTIVATE: Sweet Scent (Key {key})")
        self._press(key)

    def search_movement(self):
        """Fluid long-press movement for realistic patrolling"""
        direction = random.choice(['left', 'right'])
        # Long duration to cross multiple tiles fluidly (Human-like)
        duration = random.uniform(1.5, 3.5)
        self.log(f"Patrolling {direction.upper()} for {duration:.1f}s")
        self._press(direction, duration=duration)
        # Human pause before next action
        time.sleep(random.uniform(0.2, 0.5))

    def ditto_search_movement(self, direction):
        """Linear patrol using long continuous presses"""
        # Duration is handled by the main loop timer, but we ensure the press is solid
        duration = random.uniform(0.8, 1.5) 
        self._press(direction, duration=duration)
        # Minimal pause to maintain momentum but avoid rigid patterns
        time.sleep(random.uniform(0.05, 0.15))

    def open_fight_menu(self):
        """Press Z to enter the fight/move selection menu"""
        self.log("Opening Fight Menu (Z)")
        self._press('z')
        time.sleep(random.uniform(0.4, 0.6))

    def execute_move(self, slot):
        """Navigates a 2x2 grid: 1=TL, 2=TR, 3=BL, 4=BR"""
        self.open_fight_menu()
        self.navigate_and_confirm_move(slot)

    def navigate_and_confirm_move(self, slot):
        """Navigates 2x2 grid and confirms (Z). Assumes already in Fight Menu."""
        slot = str(slot)
        self.log(f"Navigating to Slot: {slot}")

        # Reset cursor to Top-Left
        pydirectinput.press('up')
        pydirectinput.press('left')
        time.sleep(0.2)

        if slot == '2': pydirectinput.press('right')
        elif slot == '3': pydirectinput.press('down')
        elif slot == '4': 
            pydirectinput.press('right')
            pydirectinput.press('down')
        
        time.sleep(0.2)
        self.log("Confirming Move (Z)")
        self._press('z')
        time.sleep(random.uniform(0.5, 1.0))

    def use_ball(self, key):
        """Use the quick-access ball (Hotkey)"""
        self.log(f"Using Pokeball Hotkey (Key {key})")
        self._press(key)
        time.sleep(random.uniform(0.5, 1.0))

    def use_leppa_sequence(self, key):
        """Sequence to use Leppa Berries on slots 1, 2 and 4 (legacy/counter-based)"""
        for slot in ['1', '2', '4']:
            self.use_leppa_sequence_single(key, slot)

    def use_leppa_sequence_single(self, key, slot, full_restore=False):
        """Restores PP for a specific slot using Leppa with smart navigation"""
        self.log(f"Restoring PP for Slot {slot} (Full: {full_restore})")
        
        # 1. Use Leppa Hotkey
        pydirectinput.keyDown(key)
        time.sleep(0.4)
        pydirectinput.keyUp(key)
        time.sleep(1.0)
        
        # 2. Select first Pokemon (Z)
        self._press('z')
        time.sleep(1.0)
        
        # 3. Navigate to Move Slot (1-4)
        # Reset cursor to top-left of the move list
        pydirectinput.press('up')
        pydirectinput.press('left')
        time.sleep(0.3)
        
        slot = str(slot)
        if slot == '2': pydirectinput.press('right')
        elif slot == '3': pydirectinput.press('down')
        elif slot == '4': 
            pydirectinput.press('right')
            pydirectinput.press('down')
        time.sleep(0.3)
        
        # 4. Confirm Move Selection
        self._press('z')
        time.sleep(0.8)

        # 5. Handle Quantity Submenu
        if full_restore:
            # Navigate to 'Max'
            pydirectinput.press('up')
            time.sleep(0.2)
            pydirectinput.press('right')
            time.sleep(0.2)
            self._press('z') # Select Max
            time.sleep(0.4)
            # Navigate to 'Use' and confirm
            pydirectinput.press('down')
            time.sleep(0.2)
            self._press('z')
        else:
            # Just one more Z for single berry
            self._press('z')
            
        time.sleep(2.0) # Animation delay
        self.log(f"Slot {slot} restoration complete.")

    def use_potion_sequence(self, key, full_heal=False):
        """Heals the hunter using a Potion hotkey and optional 'Max' navigation"""
        self.log(f"Healing Hunter (Full: {full_heal}) using Key {key}")
        # 1. Use Potion Hotkey
        pydirectinput.keyDown(key)
        time.sleep(0.4)
        pydirectinput.keyUp(key)
        time.sleep(1.0)
        
        # 2. Select first Pokemon (Z)
        self._press('z')
        time.sleep(0.8)
        
        if full_heal:
            # 3. Navigate to 'Max'
            pydirectinput.press('up')
            time.sleep(0.3)
            pydirectinput.press('right')
            time.sleep(0.3)
            self._press('z') # Confirm MAX
            time.sleep(0.5)
            # 4. Navigate down to 'Use' and confirm
            pydirectinput.press('down')
            time.sleep(0.3)
            self._press('z')
            time.sleep(1.5)
        else:
            # Just confirm once for single potion
            self._press('z')
            time.sleep(1.5)
            
        self.log("Healing complete.")

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
