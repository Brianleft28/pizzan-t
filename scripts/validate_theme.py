import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PIZZA_THEME_DIR = WORKSPACE_DIR / "pizzatheme"

def validate_xml_files():
    if not PIZZA_THEME_DIR.exists():
        print(f"[!] ERROR: No se encuentra el directorio del tema: {PIZZA_THEME_DIR}")
        return False
        
    all_valid = True
    for root, _, files in os.walk(PIZZA_THEME_DIR):
        for file in files:
            if file.endswith('.xml'):
                file_path = Path(root) / file
                try:
                    ET.parse(file_path)
                except ET.ParseError as e:
                    print(f"[!] ERROR SINTACTICO EN XML: {file_path.relative_to(WORKSPACE_DIR)}")
                    print(f"    Detalle: {e}")
                    all_valid = False
    return all_valid

def validate_critical_files():
    required_files = ["info.xml", "icon.png"]
    all_valid = True
    for req in required_files:
        if not (PIZZA_THEME_DIR / req).exists():
            print(f"[!] ERROR: Falta el archivo critico {req} en pizzatheme/")
            all_valid = False
    return all_valid

if __name__ == "__main__":
    print("[*] Iniciando validacion del tema...")
    xml_ok = validate_xml_files()
    files_ok = validate_critical_files()
    
    if xml_ok and files_ok:
        print("[OK] Validacion superada. El tema es integro.")
        sys.exit(0)
    else:
        print("[X] FALLO DE VALIDACION. Abortando construccion.")
        sys.exit(1)
