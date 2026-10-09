import os
import sys
import zipfile
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PIZZA_THEME_DIR = WORKSPACE_DIR / "pizzatheme"

INFO_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<resource>
    <name>PizzaTheme</name>
    <version>{revision}</version>
    <description>Pizza Theme para PokeMMO</description>
    <author>Brian/Pizzant</author>
    <themes theme_revision="8">
        <theme path="pizzatheme" name="PizzaTheme" is_mobile="false"/>
    </themes>
</resource>
"""

def get_revision(mod_dest: Path) -> str:
    # PokeMMO root is normally 3 directories up from data/mods/ (i.e. mod_dest.parent.parent.parent)
    rev_path = mod_dest.parent.parent.parent / "revision.txt"
    if rev_path.exists():
        rev = rev_path.read_text(encoding="utf-8").strip()
        print(f"[*] Revision detectada: {rev}")
        return rev
    print("[!] No se encontro revision.txt. Usando version 1 por defecto.")
    return "1"

def build_mod(target_path: str):
    mod_dest = Path(target_path)
    print(f"Empaquetando PizzaTheme en: {mod_dest} ...")
    
    if not mod_dest.parent.exists():
        mod_dest.parent.mkdir(parents=True, exist_ok=True)
        
    revision = get_revision(mod_dest)
    info_xml_content = INFO_XML_TEMPLATE.replace("{revision}", revision)
        
    with zipfile.ZipFile(mod_dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('info.xml', info_xml_content)
        
        if not PIZZA_THEME_DIR.exists():
            print("Error: No existe el directorio pizzatheme en el workspace.")
            return

        for root, dirs, files in os.walk(PIZZA_THEME_DIR):
            for file in files:
                if file == "info.xml" and Path(root) == PIZZA_THEME_DIR:
                    continue 
                
                file_path = Path(root) / file
                rel_path = file_path.relative_to(PIZZA_THEME_DIR)
                zip_path = f"pizzatheme/{rel_path}".replace("\\", "/")
                zipf.write(file_path, zip_path)

    print(f"Mod construido y copiado exitosamente en: {mod_dest}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = r"C:\Program Files\PokeMMO\data\mods\PizzaTheme.mod"
    build_mod(target)
