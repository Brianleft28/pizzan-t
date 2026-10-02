import time
from datetime import datetime, timedelta


class PokéLogger:
    """Logger con colores reales en CTkTextbox, buffer circular y niveles de verbosidad."""

    # Colores Material Dark para tags en CTkTextbox
    TAG_COLORS = {
        "INFO":    {"foreground": "#82AAFF"},
        "ACTION":  {"foreground": "#89DDFF"},
        "SUCCESS": {"foreground": "#C3E88D"},
        "WARN":    {"foreground": "#FFCB6B"},
        "FATAL":   {"foreground": "#FF5370"},
        "BATTLE":  {"foreground": "#C792EA"},
        "MAP":     {"foreground": "#B2CCD6"},
        "HEAL":    {"foreground": "#A5D6A7"},
        "DEBUG":   {"foreground": "#546E7A"},
        "HEADER":  {"foreground": "#F78C6C"},
        "PHASE":   {"foreground": "#FFCB6B"},
        "BRAIN":   {"foreground": "#82AAFF"},
    }

    PREFIXES = {
        "INFO":    "[📝]",
        "ACTION":  "[🎮]",
        "SUCCESS": "[✅]",
        "WARN":    "[⚠️]",
        "FATAL":   "[💀]",
        "BATTLE":  "[⚔️]",
        "MAP":     "[🌍]",
        "HEAL":    "[💊]",
        "DEBUG":   "[🔍]",
        "HEADER":  "[★]",
        "PHASE":   "[━]",
        "BRAIN":   "[🧠]",
    }

    # Niveles de verbosidad: qué categorías se muestran en cada nivel
    VERBOSITY_LEVELS = {
        "QUIET":   {"SUCCESS", "FATAL", "PHASE", "HEADER"},
        "NORMAL":  {"INFO", "ACTION", "SUCCESS", "WARN", "FATAL", "BATTLE", "MAP", "HEAL", "PHASE", "HEADER", "BRAIN"},
        "VERBOSE": {"INFO", "ACTION", "SUCCESS", "WARN", "FATAL", "BATTLE", "MAP", "HEAL", "DEBUG", "PHASE", "HEADER", "BRAIN"},
        "DEBUG":   {"INFO", "ACTION", "SUCCESS", "WARN", "FATAL", "BATTLE", "MAP", "HEAL", "DEBUG", "PHASE", "HEADER", "BRAIN"},
    }

    def __init__(self, text_widget=None, max_lines=2000):
        self.widget = text_widget
        self.start_time = datetime.now()
        self.max_lines = max_lines
        self.line_count = 0
        self.auto_scroll = True
        self.verbosity = "NORMAL"

        # Configurar tags de color si hay widget
        if self.widget:
            self.configure_widget(self.widget)

    def configure_widget(self, widget):
        """Configura los tags de color en un CTkTextbox."""
        self.widget = widget
        for tag_name, color_cfg in self.TAG_COLORS.items():
            try:
                widget.tag_config(tag_name, **color_cfg)
            except Exception:
                pass  # Algunas configs pueden fallar según la versión de CTk

    def get_elapsed(self):
        elapsed = datetime.now() - self.start_time
        total = int(elapsed.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}"

    def log(self, message, category="INFO"):
        """Log con color real en CTkTextbox y filtrado por verbosidad."""
        # Filtrar por verbosidad
        allowed = self.VERBOSITY_LEVELS.get(self.verbosity, self.VERBOSITY_LEVELS["NORMAL"])
        if category not in allowed:
            return

        timer = self.get_elapsed()
        prefix = self.PREFIXES.get(category, "[•]")

        # Limpiar mensajes que ya traen formato anidado del controller
        clean_msg = str(message).strip()
        if clean_msg.startswith("[🎮]"):
            clean_msg = clean_msg[4:].strip()

        formatted = f"[{timer}] {prefix} {clean_msg}"

        if self.widget:
            try:
                # Insertar con tag de color
                self.widget.insert("end", formatted + "\n", category)
                self.line_count += 1

                # Auto-scroll
                if self.auto_scroll:
                    self.widget.see("end")

                # Buffer circular
                self._trim_buffer()
            except Exception:
                pass  # Widget puede estar siendo destruido
        else:
            # Fallback a consola con ANSI colors
            ansi = {
                "INFO": "\033[94m", "ACTION": "\033[96m", "SUCCESS": "\033[92m",
                "WARN": "\033[93m", "FATAL": "\033[91m", "BATTLE": "\033[95m",
                "MAP": "\033[97m", "HEAL": "\033[92m", "DEBUG": "\033[90m",
                "HEADER": "\033[93m", "PHASE": "\033[93m", "BRAIN": "\033[94m",
            }
            color = ansi.get(category, "")
            try:
                print(f"{color}{formatted}\033[0m")
            except UnicodeEncodeError:
                # Si falla el encoding en PowerShell por los emojis, limpiamos los caracteres
                clean_ascii = formatted.encode('ascii', 'replace').decode('ascii')
                print(f"{color}{clean_ascii}\033[0m")

    def log_phase(self, phase_name):
        """Inserta un separador visual de fase."""
        separator = f"━━━━━━━━━━ {phase_name} ━━━━━━━━━━"
        self.log(separator, "PHASE")

    def _trim_buffer(self):
        """Elimina líneas viejas si excede el máximo."""
        if self.line_count > self.max_lines:
            try:
                excess = self.line_count - self.max_lines
                self.widget.delete("1.0", f"{excess + 1}.0")
                self.line_count = self.max_lines
            except Exception:
                pass

    def clear(self):
        """Limpia todo el contenido del log."""
        if self.widget:
            try:
                self.widget.delete("1.0", "end")
                self.line_count = 0
            except Exception:
                pass

    def clear_start_time(self):
        self.start_time = datetime.now()

    def get_last_lines(self, count=10):
        if not self.widget:
            return ""
        try:
            content = self.widget.get("1.0", "end-1c")
            lines = [l for l in content.split("\n") if l.strip()]
            return "\n".join(lines[-count:])
        except Exception:
            return ""
