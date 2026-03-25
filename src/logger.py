import time
from datetime import datetime, timedelta

class PokéLogger:
    def __init__(self, text_widget=None):
        self.widget = text_widget
        self.start_time = datetime.now()
        
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
        
        # Evitamos que se aniden los logs si el mensaje ya trae formato
        clean_msg = str(message).strip()
        full_line = f"[{timer}] {prefix} {clean_msg}"
        
        if self.widget:
            self.widget.insert("end", f"{full_line}\n")
            self.widget.see("end")
        else:
            print(full_line)

    def clear_start_time(self):
        self.start_time = datetime.now()
