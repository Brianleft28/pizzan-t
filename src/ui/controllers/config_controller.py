import os
import json
from src.ui.models.config_model import AppConfig

class ConfigController:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load()

    def load(self) -> AppConfig:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return AppConfig.from_dict(data)
            except Exception as e:
                print(f"[!] Error loading {self.config_path}: {e}")
        return AppConfig()

    def save(self, config: AppConfig) -> bool:
        self.config = config
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config.to_dict(), f, indent=4)
            return True
        except Exception as e:
            print(f"[!] Error saving {self.config_path}: {e}")
            return False

    def get_val(self, key: str, default=""):
        return getattr(self.config, key, default)
