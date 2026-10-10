import os
import sys
import zipfile
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PIZZA_THEME_DIR = WORKSPACE_DIR / "pizzatheme"

INFO_XML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<resource name="PizzaTheme" version="{revision}" description="Pizza Theme para PokeMMO" author="Brian/Pizzant">
    <themes>
        <theme path="pizzatheme" name="PizzaTheme" revision="8" is_mobile="false" sprite_atlas="pizzatheme/atlas/main.atlas"/>
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
                # We must include the theme's own info.xml inside its folder
                # so PokeMMO recognizes it as a valid theme inside the mod.
                pass
                
                file_path = Path(root) / file
                rel_path = file_path.relative_to(PIZZA_THEME_DIR)
                zip_path = f"pizzatheme/{rel_path}".replace("\\", "/")
                zipf.write(file_path, zip_path)
                
                # Copy icon.png to the root so PokeMMO Mod Manager displays the logo
                if file == "icon.png" and Path(root) == PIZZA_THEME_DIR:
                    zipf.write(file_path, "icon.png")

    print(f"Mod construido y copiado exitosamente en: {mod_dest}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = r"C:\Program Files\PokeMMO\data\mods\PizzaTheme.mod"
    build_mod(target)
