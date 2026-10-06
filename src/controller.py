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

        # --- ANTI-COLLISION: Estado de patrullaje ---
        self.last_patrol_direction = random.choice(['left', 'right'])
        self.patrol_axis_start_time = time.time()
        # Segundos máximos caminando en el mismo eje sin encuentro antes de asumir colisión
        self.collision_timeout_sec = float(self.controls.get("collision_timeout", 12.0))
        self._collision_count = 0  # Contador de colisiones consecutivas

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

    def reset_patrol_timer(self):
        """Llamar cuando el bot entra en combate o detecta actividad real.
        Resetea el timer anti-colisión para que no dispare un cambio innecesario."""
        self.patrol_axis_start_time = time.time()
        self._collision_count = 0

    def _handle_collision(self):
        """Ejecuta la maniobra anti-colisión: micro-retroceso + cambio de eje."""
        self._collision_count += 1
        old_dir = self.last_patrol_direction

        # Micro-retroceso: dar un paso corto en la dirección opuesta
        opposite = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        retreat_dir = opposite.get(old_dir, 'right')
        self.log(f"🧱 ANTI-COLLISION #{self._collision_count}: Wall detected! Retreating {retreat_dir.upper()}")
        self._press(retreat_dir, duration=random.uniform(0.3, 0.6))
        time.sleep(random.uniform(0.1, 0.3))

        # Cambio de eje: si estábamos en horizontal, pasar a vertical y viceversa
        if old_dir in ['left', 'right']:
            self.last_patrol_direction = random.choice(['up', 'down'])
        else:
            self.last_patrol_direction = random.choice(['left', 'right'])

        self.log(f"🧭 ANTI-COLLISION: Axis change {old_dir.upper()} → {self.last_patrol_direction.upper()}")
        self.patrol_axis_start_time = time.time()

        # Si llevamos muchas colisiones seguidas, hacer un movimiento largo para escapar de la esquina
        if self._collision_count >= 3:
            self.log("⚠️ ANTI-COLLISION: Corner escape! Long diagonal movement")
            escape_dir = random.choice(['left', 'right', 'up', 'down'])
            self._press(escape_dir, duration=random.uniform(2.5, 4.0))
            self._collision_count = 0
            self.last_patrol_direction = escape_dir
            self.patrol_axis_start_time = time.time()

    def search_movement(self):
        """Fluid long-press movement for realistic patrolling — con anti-colisión por timeout."""
        # Verificar si excedimos el timeout en el mismo eje (posible pared)
        elapsed_on_axis = time.time() - self.patrol_axis_start_time
        if elapsed_on_axis > self.collision_timeout_sec:
            self._handle_collision()

        direction = self.last_patrol_direction

        # Variación humana: cambio ocasional de sentido dentro del mismo eje
        if random.random() > 0.8:
            opposite = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
            direction = opposite.get(direction, direction)

        # Long duration to cross multiple tiles fluidly (Human-like)
        duration = random.uniform(1.5, 3.5)
        self.log(f"Patrolling {direction.upper()} for {duration:.1f}s")
        self._press(direction, duration=duration)
        # Human pause before next action
        time.sleep(random.uniform(0.2, 0.5))

    def ditto_search_movement(self, direction):
        """Linear patrol using long continuous presses — con tracking anti-colisión."""
        # Actualizar dirección trackeada
        if direction != self.last_patrol_direction:
            self.last_patrol_direction = direction
            self.patrol_axis_start_time = time.time()

        # Verificar timeout
        elapsed_on_axis = time.time() - self.patrol_axis_start_time
        if elapsed_on_axis > self.collision_timeout_sec:
            self._handle_collision()
            direction = self.last_patrol_direction  # Usar la nueva dirección

        # Duration is handled by the main loop timer, but we ensure the press is solid
        duration = random.uniform(0.8, 1.5)
        self._press(direction, duration=duration)
        # Minimal pause to maintain momentum but avoid rigid patterns
        time.sleep(random.uniform(0.05, 0.15))

    def open_fight_menu(self):
        """Press Z to enter the fight/move selection menu"""
        self.log("Opening Fight Menu (Z)")
        self._press('z')
        time.sleep(random.uniform(0.2, 0.4))

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
        time.sleep(random.uniform(0.1, 0.2))

        if slot == '2': pydirectinput.press('right')
        elif slot == '3': pydirectinput.press('down')
        elif slot == '4': 
            pydirectinput.press('right')
            pydirectinput.press('down')
        
        time.sleep(random.uniform(0.1, 0.2))
        self.log("Confirming Move (Z)")
        self._press('z')
        time.sleep(random.uniform(0.3, 0.6))

    def use_ball(self, key):
        """Use the quick-access ball (Hotkey)"""
        self.log(f"Using Pokeball Hotkey (Key {key})")
        self._press(key)
        time.sleep(random.uniform(0.3, 0.6))

    def use_leppa_sequence(self, key):
        """Sequence to use Leppa Berries on slots 1, 2 and 4 (legacy/counter-based)"""
        for slot in ['1', '2', '4']:
            self.use_leppa_sequence_single(key, slot)

    def use_leppa_sequence_single(self, key, slot, full_restore=False):
        """Restores PP for a specific slot using Leppa with smart navigation"""
        self.log(f"Restoring PP for Slot {slot} (Full: {full_restore})")
        
        # 1. Use Leppa Hotkey
        pydirectinput.keyDown(key)
        time.sleep(random.uniform(0.1, 0.3))
        pydirectinput.keyUp(key)
        time.sleep(random.uniform(0.6, 0.9))
        
        # 2. Select first Pokemon (Z)
        self._press('z')
        time.sleep(random.uniform(0.6, 1.0))
        
        # 3. Navigate to Move Slot (1-4)
        # Reset cursor to top-left of the move list
        pydirectinput.press('up')
        pydirectinput.press('left')
        time.sleep(random.uniform(0.1, 0.25))
        
        slot = str(slot)
        if slot == '2': pydirectinput.press('right')
        elif slot == '3': pydirectinput.press('down')
        elif slot == '4': 
            pydirectinput.press('right')
            pydirectinput.press('down')
        time.sleep(random.uniform(0.1, 0.25))
        
        # 4. Confirm Move Selection
        self._press('z')
        time.sleep(random.uniform(0.5, 0.8))

        # 5. Handle Quantity Submenu
        if full_restore:
            # Navigate to 'Max'
            pydirectinput.press('up')
            time.sleep(random.uniform(0.1, 0.2))
            pydirectinput.press('right')
            time.sleep(random.uniform(0.1, 0.2))
            self._press('z') # Select Max
            time.sleep(random.uniform(0.1, 0.3))
            # Navigate to 'Use' and confirm
            pydirectinput.press('down')
            time.sleep(random.uniform(0.1, 0.2))
            self._press('z')
        else:
            # Just one more Z for single berry
            self._press('z')
            
        time.sleep(random.uniform(1.2, 1.8)) # Animation delay
        self.log(f"Slot {slot} restoration complete.")


    def run_away(self):
        """Navigates to the 'RUN' button with detailed logs and micro-delays to prevent input swallows"""
        path_id = random.randint(0, 3)
        self.log(f"ESCAPE PROTOCOL: Route {path_id}")
        
        # 1. Reset menu with micro-delays
        self._press('x', duration=0.05)
        time.sleep(random.uniform(0.05, 0.15))
        self._press('up', duration=0.05)
        time.sleep(random.uniform(0.05, 0.15))
        self._press('left', duration=0.05)
        time.sleep(random.uniform(0.05, 0.15))

        # 2. Routes
        if path_id == 0: # Direct
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
        elif path_id == 1: # Inverse
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
        elif path_id == 2: # Redundant
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
        else: # Doubt
            self._press('down', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            self._press('right', duration=0.05); time.sleep(random.uniform(0.05, 0.1))
            
        self.log("CONFIRM: Running away (Z)")
        self._press('z')
        
        if random.random() > 0.6:
            self._press('x')
