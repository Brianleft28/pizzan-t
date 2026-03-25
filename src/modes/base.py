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

    def _wait_for_menu(self, timeout=30):
        """Utilidad común para esperar a que el menú de batalla esté listo"""
        start = time.time()
        while (time.time() - start) < timeout:
            if not self.bot.running: return False
            if self.bot.is_menu_ready(self.observer.capture_frame()):
                return True
            time.sleep(0.2)
        return False
