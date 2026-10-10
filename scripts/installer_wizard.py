import os
import sys
import shutil
import zipfile
import json
import time
import subprocess
import re
from pathlib import Path

try:
    import questionary
except ImportError:
    print("Falta questionary. Instalalo con pip install questionary.")
    sys.exit(1)

def print_yandere(msg, color="white"):
    colors = {
        "white": "\033[97m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "reset": "\033[0m"
    }
    c = colors.get(color, colors["white"])
    print(f"{c}{msg}{colors['reset']}")

def sync_xml(xml_path, game_ver):
    try:
        with open(xml_path, "r", encoding="utf-8") as f:
            xml_data = f.read()
            
        # Sincronizar theme revision="8"
        if '<theme' in xml_data and 'revision="' not in xml_data:
            xml_data = re.sub(r'<theme([^>]*)>', r'<theme revision="8"\1>', xml_data)
        elif '<theme' in xml_data:
            xml_data = re.sub(r'revision="[^"]*"', 'revision="8"', xml_data)
            
        # Sincronizar resource version="8" para mods como Moonlyze
        if '<resource' in xml_data and 'version="' not in xml_data:
            xml_data = re.sub(r'<resource([^>]*)>', r'<resource version="8"\1>', xml_data)
        elif '<resource' in xml_data:
            xml_data = re.sub(r'version="[^"]*"', 'version="8"', xml_data)
            
        # Sincronizar la etiqueta <version> (para temas y mods viejos)
        if '<version>' in xml_data:
            xml_data = re.sub(r'<version>[^<]*</version>', f'<version>{game_ver}</version>', xml_data)
            
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        return True
    except Exception as e:
        print_yandere(f"  [X] Fallo parseando {xml_path}: {e}", "red")
        return False

def main():
    os.system("color") 
    print_yandere("\n[♥] ¡Hola bebito! Preparando la magia interactiva...", "magenta")
    print_yandere("    完璧 (かんぺき - Kanpeki) - [Perfecto]\n", "magenta")

    base_dir = Path(__file__).parent.parent.absolute()
    
    # 1. Encontrar PokeMMO
    default_paths = [
        r"C:\PokeMMO",
        r"D:\PokeMMO",
        r"C:\Program Files\PokeMMO",
        os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "PokeMMO")
    ]
    
    found_paths = [p for p in default_paths if os.path.exists(os.path.join(p, "revision.txt"))]
    choices = found_paths + ["Ingresar otra ruta manualmente"]
    
    target = questionary.select(
        "Che pibe, ¿dónde tenés el PokeMMO?",
        choices=choices
    ).ask()

    if target == "Ingresar otra ruta manualmente":
        target = questionary.path("Pasame la ruta de PokeMMO (donde está revision.txt):").ask()

    if not target or not os.path.exists(os.path.join(target, "revision.txt")):
        print_yandere("[X] Esa ruta no tiene PokeMMO, bebito. ¡No me mientas!", "red")
        sys.exit(1)

    print_yandere(f"[OK] Laburando en: {target}", "cyan")
    
    # Obtener version
    with open(os.path.join(target, "revision.txt"), "r", encoding="utf-8") as f:
        game_ver = f.read().strip()
    
    # 2. Roms (ZIP Support)
    desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    zip_files = list(desktop.glob("*okemmo*.zip")) + list(desktop.glob("*rom*.zip")) + list(desktop.glob("*.zip"))
    zip_choices = list(set([str(z) for z in zip_files]))
    
    rom_zip = questionary.select(
        "¿De dónde saco las ROMs y el fondo negro modificado (patchedfile.nds)?",
        choices=zip_choices + ["Seleccionar otro ZIP", "Skipiame esto, ya tengo las ROMs puestas"]
    ).ask()
    
    if rom_zip == "Seleccionar otro ZIP":
        rom_zip = questionary.path("Pasame la ruta exacta del ZIP con las ROMs:").ask()
        
    if rom_zip and rom_zip != "Skipiame esto, ya tengo las ROMs puestas":
        print_yandere(f"[⚙️] Extrayendo ROMs desde {rom_zip}...", "yellow")
        rom_dest = os.path.join(target, "roms")
        os.makedirs(rom_dest, exist_ok=True)
        
        try:
            with zipfile.ZipFile(rom_zip, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    # Ignorar directorios, solo extraer archivos (nds, gba) a la raiz de roms
                    if not file_info.is_dir() and file_info.filename.lower().endswith(('.nds', '.gba')):
                        file_info.filename = os.path.basename(file_info.filename)
                        if file_info.filename:
                            zip_ref.extract(file_info, rom_dest)
            print_yandere("  [OK] ROMs inyectadas (NDS y GBA).", "green")
        except Exception as e:
            print_yandere(f"  [X] Hubo un re bardo extrayendo el ZIP: {e}", "red")
            
    # 3. Theme Injection
    print_yandere("[⚙️] Inyectando el PizzaTheme...", "yellow")
    theme_source = os.path.join(base_dir, "PizzaTheme")
    theme_dest = os.path.join(target, "data", "themes", "PizzaTheme")
    
    bad_mod = os.path.join(target, "data", "mods", "PizzaTheme.mod")
    bad_zip = os.path.join(target, "data", "themes", "PizzaTheme.zip")
    if os.path.exists(bad_mod): os.remove(bad_mod)
    if os.path.exists(bad_zip): os.remove(bad_zip)
    
    if os.path.exists(theme_dest):
        shutil.rmtree(theme_dest)
    shutil.copytree(theme_source, theme_dest)
    print_yandere("  [OK] PizzaTheme inyectado. Basadísimo.", "green")
    
    # 4. XML Version Sync Universal
    print_yandere(f"[⚙️] Sincronizando metadatos XML para PokeMMO Rev {game_ver}...", "yellow")
    
    targets = [
        Path(target) / "data" / "mods",
        Path(target) / "data" / "themes"
    ]
    for d in targets:
        if d.is_dir():
            for xml_file in d.rglob("info.xml"):
                if sync_xml(xml_file, game_ver):
                    print_yandere(f"  [OK] XML Sync: {xml_file.parent.name}", "green")
        
    # 5. Force Theme Selection
    main_props = os.path.join(target, "config", "main.properties")
    if os.path.exists(main_props):
        with open(main_props, "r", encoding="utf-8") as f:
            props = f.read()
        if 'client.ui.theme=' in props:
            props = re.sub(r'^client\.ui\.theme=.*', 'client.ui.theme=PizzaTheme', props, flags=re.MULTILINE)
        else:
            props += "\nclient.ui.theme=PizzaTheme\n"
        with open(main_props, "w", encoding="utf-8") as f:
            f.write(props)
        print_yandere("  [OK] client.ui.theme = PizzaTheme. Cero complacencia, yo decido.", "green")

    # 6. Patcher
    print_yandere("[⚙️] Instalando el Patcher de UI...", "magenta")
    patcher_dir = os.path.join(base_dir, "scripts", "patcher")
    patcher_config = os.path.join(patcher_dir, "patcher_config.json")
    
    if os.path.exists(patcher_config):
        with open(patcher_config, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        config["game_path"] = target
        if "PizzaTheme" not in config.get("themes", []):
            config.setdefault("themes", []).append("PizzaTheme")
            
        with open(patcher_config, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
            
    patcher_mod_dest = os.path.join(target, "data", "mods", "pokemmo_ui_patcher")
    if os.path.exists(patcher_mod_dest):
        shutil.rmtree(patcher_mod_dest)
    shutil.copytree(patcher_dir, patcher_mod_dest)
    
    print_yandere("  [OK] Patcher instalado en mods.", "green")
    
    print_yandere("\n[⚙️] Ejecutando el Patcher (mod de medidas)...", "yellow")
    patcher_main = os.path.join(patcher_dir, "main.py")
    try:
        subprocess.run([sys.executable, patcher_main], check=True)
        print_yandere("\n[♥] ¡Todo listo, bebito! El Pizza Theme y sus medidas están god.", "green")
        print_yandere("    私があなたを守る (わたしがあなたをまもる - Watashi ga anata o mamoru) - [Yo te protegeré]. A viciar.", "green")
    except subprocess.CalledProcessError:
        print_yandere("\n[X] Falló el patcher... arreglalo o te juro que rompo todo.", "red")
        
if __name__ == "__main__":
    main()
