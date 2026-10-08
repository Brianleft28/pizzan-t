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
        else:
            print("[!] Advertencia: No se encontro COMO_INSTALAR.txt")
            
        if MODS_DIR.exists():
            for root, dirs, files in os.walk(MODS_DIR):
                for file in files:
                    if file.endswith(".mod"):
                        file_path = Path(root) / file
                        zipf.write(file_path, f"mods/{file}")
        else:
            print("[!] Advertencia: No se encontro la carpeta mods/")
            
    print("[OK] Release generado exitosamente. Listo para distribuir.")

if __name__ == "__main__":
    build_release()
