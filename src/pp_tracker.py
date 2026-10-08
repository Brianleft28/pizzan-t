import json
import os
import time

class PPTracker:
    def __init__(self, log_callback, config_path="config.json"):
        self.log = log_callback
        self.config_path = config_path
        self.state_file = "pp_state.json"
        
        # Cargar los maximos configurados
        self.max_pp = self._load_max_pp()
        # Cargar el estado actual o crearlo
        self.current_pp = self._load_state()

    def _load_max_pp(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    cfg = json.load(f)
                    return {
                        "sweet_scent": int(cfg.get("pp_max_sweet_scent", 32)),
                        "spore": int(cfg.get("pp_max_spore", 15)),
                        "swipe": int(cfg.get("pp_max_swipe", 40))
                    }
        except Exception as e:
            self.log(f"[PPTracker] Error al cargar maximos: {e}", "WARN")
            
        return {"sweet_scent": 32, "spore": 15, "swipe": 40}

    def _load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, "r") as f:
                    return json.load(f)
        except:
            pass
        
        # Si no existe, asume maximos
        return {
            "sweet_scent": self.max_pp["sweet_scent"],
            "spore": self.max_pp["spore"],
            "swipe": self.max_pp["swipe"]
        }

    def _save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.current_pp, f, indent=4)
        except Exception as e:
            self.log(f"[PPTracker] Error al guardar estado: {e}", "WARN")

    def get_pp(self, move_name):
        return self.current_pp.get(move_name, 99)

    def decrement_pp(self, move_name):
        if move_name in self.current_pp:
            self.current_pp[move_name] = max(0, self.current_pp[move_name] - 1)
            self.log(f"[PP Tracker] {move_name.upper()} PP: {self.current_pp[move_name]}/{self.max_pp.get(move_name, '?')}", "DEBUG")
            self._save_state()

    def restore_pp(self, move_name):
        if move_name in self.current_pp:
            self.current_pp[move_name] = self.max_pp[move_name]
            self.log(f"[PP Tracker] {move_name.upper()} restaurado a {self.max_pp[move_name]} PP.", "HEAL")
            self._save_state()
