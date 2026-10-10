import os
import re
from pathlib import Path

class PokeMMOClient:
    def __init__(self):
        self.target_dir = None
        self.game_ver = None

    def auto_detect(self):
        default_paths = [
            r"C:\PokeMMO",
            r"D:\PokeMMO",
            r"C:\Program Files\PokeMMO",
            os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "PokeMMO")
        ]
        found_paths = [p for p in default_paths if os.path.exists(os.path.join(p, "revision.txt"))]
        
        if len(found_paths) == 1:
            self.target_dir = found_paths[0]
            self._load_version()
            return True
        return False

    def set_target(self, path):
        if os.path.exists(os.path.join(path, "revision.txt")):
            self.target_dir = path
            self._load_version()
            return True
        return False

    def _load_version(self):
        with open(os.path.join(self.target_dir, "revision.txt"), "r", encoding="utf-8-sig") as f:
            self.game_ver = f.read().strip()

    def get_roms_dir(self):
        return os.path.join(self.target_dir, "roms")
        
    def get_themes_dir(self):
        return os.path.join(self.target_dir, "data", "themes")

    def get_mods_dir(self):
        return os.path.join(self.target_dir, "data", "mods")

    def force_theme(self, theme_name):
        main_props = os.path.join(self.target_dir, "config", "main.properties")
        if os.path.exists(main_props):
            with open(main_props, "r", encoding="utf-8-sig") as f:
                props = f.read()
            if 'client.ui.theme=' in props:
                props = re.sub(r'^client\.ui\.theme=.*', f'client.ui.theme={theme_name}', props, flags=re.MULTILINE)
            else:
                props += f"\nclient.ui.theme={theme_name}\n"
            with open(main_props, "w", encoding="utf-8") as f:
                f.write(props)
            return True
        return False
