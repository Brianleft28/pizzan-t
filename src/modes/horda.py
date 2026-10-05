import time
import cv2
from src.modes.base import HuntingMode

class HordeMode(HuntingMode):
    def __init__(self, bot):
        super().__init__(bot)

    def execute(self, frame):
        # 1. Mapa — usar Sweet Scent
        if not self.bot.is_menu_ready(frame) and not self.bot.check_any_name_visible(frame):
            self.log("━━━━━ 🌺 SWEET SCENT ━━━━━", "PHASE")
            self.controller.use_sweet_scent()
            time.sleep(5.0)
            return

        # 2. Batalla — esperar menú
        if not self.bot.is_menu_ready(frame):
            if not self._wait_for_menu(): return

        # 3. ESCANEO UNIVERSAL (MANDATO 6)
        self.log("━━━━━ ⚔️ HORDE BATTLE ━━━━━", "PHASE")
        
        # Pausa extra si se caza Zorua (por animaciones de disfraz/ilusión)
        if self.bot.config.get("mode_zorua", False):
            z_wait = self.bot.config.get("zorua_wait", 2.5)
            self.log(f"🦊 Modo Zorua Activo: Esperando {z_wait}s a que se asiente el disfraz...", "DEBUG")
            time.sleep(z_wait)

        f_bat = self.observer.capture_frame()
        shiny_found, target_name, all_names, slot_id = self.bot.scan_all_potential_targets(f_bat)
        
        # Log compacto del scan
        preview = ", ".join([n.upper() for n in all_names[:3]])
        suffix = "..." if len(all_names) > 3 else ""
        self.log(f"Scan: {len(all_names)} target(s) → {preview}{suffix}", "BATTLE")

        if shiny_found:
            self.log(f"━━━━━ ✨ SHINY IN HORDE! ━━━━━", "PHASE")
            self.log(f"✨ SHINY: {target_name.upper()} (Slot: {slot_id}) ✨", "SUCCESS")
            cv2.imwrite("shiny_detected.png", f_bat)
            self.bot.send_discord_alert("HORDE", f"SHINY {target_name}!", "shiny_detected.png")
            self.bot.panic_stop()
            return

        # 4. Escape
        h_size = self.bot.config.get("horde_size", 5)
        self.controller.run_away()
        self._wait_for_map()
        self.bot.encounters += int(h_size)
        self.bot.save_progress()
        self.log(f"💨 No shiny. Escaped. [Enc #{self.bot.encounters} | Horde +{h_size}]", "ACTION")
        time.sleep(1.5)

    def _wait_for_map(self):
        esc_start = time.time()
        while self.bot.check_any_name_visible(self.observer.capture_frame()) and self.bot.running:
            if time.time() - esc_start > 5.0: break
            time.sleep(0.5)
        time.sleep(1.0)
