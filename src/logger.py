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
        
        self.colors = {
            "INFO":    "\033[94m", # Blue
            "ACTION":  "\033[96m", # Cyan
            "SUCCESS": "\033[92m", # Green
            "WARN":    "\033[93m", # Yellow
            "FATAL":   "\033[91m", # Red
            "BATTLE":  "\033[95m", # Magenta
            "MAP":     "\033[97m", # White
            "HEAL":    "\033[92m", # Green
            "DEBUG":   "\033[90m", # Gray
        }
        self.reset = "\033[0m"

    def get_elapsed(self):
        elapsed = datetime.now() - self.start_time
        return str(timedelta(seconds=int(elapsed.total_seconds())))

    def log(self, message, category="INFO"):
        timer = self.get_elapsed()
        prefix = self.prefixes.get(category, "[•]")
        color = self.colors.get(category, self.reset)
        
        # Evitamos que se aniden los logs si el mensaje ya trae formato
        clean_msg = str(message).strip()
        if clean_msg.startswith("[🎮]"): clean_msg = clean_msg[4:].strip()
        
        if self.widget:
            self.widget.insert("end", f"[{timer}] {prefix} {clean_msg}\n")
            self.widget.see("end")
        else:
            # Consola a color
            print(f"{color}[{timer}] {prefix} {clean_msg}{self.reset}")

    def clear_start_time(self):
        self.start_time = datetime.now()

    def get_last_lines(self, count=10):
        if not self.widget: return ""
        try:
            content = self.widget.get("1.0", "end-1c")
            lines = [l for l in content.split("\n") if l.strip()]
            return "\n".join(lines[-count:])
        except:
            return ""
