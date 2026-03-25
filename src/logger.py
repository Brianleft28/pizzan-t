import time
from datetime import datetime, timedelta

class PokéLogger:
    def __init__(self, text_widget=None):
        self.widget = text_widget
        self.start_time = datetime.now()
        
        # Prefijos ASCII con estilo
        self.prefixes = {
            "INFO":    "[📝]",
            "ACTION":  "[🎮]",
            "SUCCESS": "[✅]",
            "WARN":    "[⚠️]",
            "FATAL":   "[💀]",
            "BATTLE":  "[⚔️]",
            "MAP":     "[🌍]",
            "HEAL":    "[💊]",
            "DEBUG":   "[🔍]"
        }

    def get_elapsed(self):
        elapsed = datetime.now() - self.start_time
        return str(timedelta(seconds=int(elapsed.total_seconds())))

    def log(self, message, category="INFO"):
        timer = self.get_elapsed()
        prefix = self.prefixes.get(category, "[•]")
        full_msg = f"[{timer}] {prefix} {message}"
        
        if self.widget:
            self.widget.insert("end", f"{full_msg}\n")
            self.widget.see("end")
        else:
            print(full_msg)

    def clear_start_time(self):
        self.start_time = datetime.now()
