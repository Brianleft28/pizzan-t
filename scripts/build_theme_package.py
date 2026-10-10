import os
import sys
import zipfile
import shutil
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

# Añadir el subdirectorio patcher al path para poder importar sus modulos
sys.path.append(str(Path(__file__).parent / "patcher"))

from patcher.xml_engine import apply_patch
from patcher.config import PATCH_TARGETS

WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PIZZATHEME_SOURCE = WORKSPACE_DIR / "pizzatheme"

# Texturas e imágenes a inyectar siempre
INJECT_ASSETS = [
    ("textures/login_bg.png", PIZZATHEME_SOURCE / "textures" / "login_bg.png"),
    ("textures/logo.png", PIZZATHEME_SOURCE / "textures" / "logo.png"),
    ("icon.png", PIZZATHEME_SOURCE / "icon.png")
]

# Parches que aplicaremos sí o sí al tema base usando la lógica de pokemmo_ui_patcher
# Puedes ajustar estos valores a los que vos querías
APPLY_PATCHES = {
    "pc": {
        "boxWidth": "1000",
        "boxHeight": "600",
        "partyWidth": "250",
        "partyHeight": "600"
    },
    "bag": {
        "bagWidth": "600",
        "bagHeight": "500"
    },
    "summary": {
        "summaryWidth": "800",
        "summaryHeight": "500"
    }
}

def generate_info_xml(theme_internal_name: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<resource name="PizzaTheme" version="1" description="Pizza Theme" author="Pizzant">
    <themes>
        <theme path="{theme_internal_name}" name="PizzaTheme" revision="8" is_mobile="false" sprite_atlas="atlas/main.atlas"/>
    </themes>
</resource>"""

def build_package(base_zip_path: str):
    if not Path(base_zip_path).exists():
        print(f"[!] Error: No se encontró el archivo base {base_zip_path}")
        sys.exit(1)

    output_zip = WORKSPACE_DIR / "PizzaTheme.zip"

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        
        print(f"[*] Extrayendo tema base desde {base_zip_path}...")
        with zipfile.ZipFile(base_zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
            
        # Detectar cuál es la carpeta interna del tema base (ej: Moonlyze99)
        # Buscamos la carpeta que contiene el archivo 'theme.xml'
        theme_internal_dir = None
        for root, dirs, files in os.walk(tmpdir):
            if "theme.xml" in files:
                theme_internal_dir = Path(root)
                break
                
        if not theme_internal_dir:
            print("[!] Error: No se encontró 'theme.xml' en el ZIP base. ¿Es un tema válido de PokeMMO?")
            sys.exit(1)
            
        internal_name = theme_internal_dir.name
        print(f"[*] Detectada carpeta interna del tema: {internal_name}")
        
        print("[*] Inyectando assets de PizzaTheme (login_bg.png, logo.png, icon.png)...")
        for rel_dest, src_path in INJECT_ASSETS:
            if src_path.exists():
                dest = theme_internal_dir / rel_dest
                # icon.png va en el root junto al info.xml normalmente, pero lo ponemos donde va
                if rel_dest == "icon.png":
                    dest = tmpdir / "icon.png"
                    
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dest)
                print(f"    -> Copiado {src_path.name}")
            else:
                print(f"    [!] Faltó {src_path.name} en el workspace, saltando...")

        # También copiamos la carpeta atlas si la tenemos
        atlas_src = PIZZATHEME_SOURCE / "atlas"
        if atlas_src.exists():
            atlas_dest = tmpdir / "atlas"
            if atlas_dest.exists():
                shutil.rmtree(atlas_dest)
            shutil.copytree(atlas_src, atlas_dest)
            print("    -> Atlas inyectado.")

        print("[*] Parcheando XMLs dinámicamente con UI Patcher...")
        for target_key, new_values in APPLY_PATCHES.items():
            target_def = PATCH_TARGETS.get(target_key)
            if not target_def:
                continue
            xml_path = theme_internal_dir / target_def.xml_file
            if xml_path.exists():
                try:
                    changes = apply_patch(xml_path, target_def, new_values)
                    print(f"    -> {target_def.label} parcheado exitosamente.")
                except Exception as e:
                    print(f"    [!] Fallo al parchear {target_def.label}: {e}")
            else:
                print(f"    [!] Archivo no encontrado: {target_def.xml_file}")

        print("[*] Generando info.xml (revisión 8)...")
        info_xml_path = tmpdir / "info.xml"
        info_xml_path.write_text(generate_info_xml(internal_name), encoding="utf-8")
        
        print(f"[*] Re-empaquetando PizzaTheme.zip...")
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(tmpdir)
                    zipf.write(file_path, str(rel_path).replace("\\", "/"))

    print(f"\n[Exito] Paquete forjado: {output_zip}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python build_theme_package.py <ruta_al_zip_base>")
        sys.exit(1)
    
    build_package(sys.argv[1])
