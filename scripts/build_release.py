import os
import zipfile
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
MODS_DIR = WORKSPACE_DIR / "mods"
RELEASE_ZIP = WORKSPACE_DIR / "Release_PizzaTheme.zip"
INSTRUCTIONS = WORKSPACE_DIR / "COMO_INSTALAR.txt"

def build_release():
    print(f"Empaquetando release en: {RELEASE_ZIP}")
    
    with zipfile.ZipFile(RELEASE_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if INSTRUCTIONS.exists():
            zipf.write(INSTRUCTIONS, "COMO_INSTALAR.txt")
            
        if MODS_DIR.exists():
            for root, dirs, files in os.walk(MODS_DIR):
                for file in files:
                    if file.endswith(".mod"):
                        file_path = Path(root) / file
                        zipf.write(file_path, f"mods/{file}")
                        
        PIZZA_THEME_DIR = WORKSPACE_DIR / "pizzatheme"
        if PIZZA_THEME_DIR.exists():
            for root, dirs, files in os.walk(PIZZA_THEME_DIR):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(PIZZA_THEME_DIR)
                    zipf.write(file_path, f"themes/PizzaTheme/{rel_path}")
            
    print("[OK] Release generado exitosamente. Listo para distribuir.")

if __name__ == "__main__":
    build_release()
