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

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    console = Console()
except ImportError:
    print("Falta rich. Instalalo con pip install rich.")
    sys.exit(1)

def print_step(msg, style="bold yellow"):
    console.print(f"[{style}]>> {msg}[/]")

def print_success(msg):
    console.print(f"[bold green][OK] {msg}[/]")

def print_error(msg):
    console.print(f"[bold red][ERR] {msg}[/]")

def sync_xml(xml_path, game_ver):
    try:
        with open(xml_path, "r", encoding="utf-8-sig") as f:
            xml_data = f.read()
            
        if '<theme' in xml_data and 'revision="' not in xml_data:
            xml_data = re.sub(r'<theme([^>]*)>', r'<theme revision="8"\1>', xml_data)
        elif '<theme' in xml_data:
            xml_data = re.sub(r'revision="[^"]*"', 'revision="8"', xml_data)
            
        if '<resource' in xml_data and 'version="' not in xml_data:
            xml_data = re.sub(r'<resource([^>]*)>', r'<resource version="8"\1>', xml_data)
        elif '<resource' in xml_data:
            xml_data = re.sub(r'version="[^"]*"', 'version="8"', xml_data)
            
        if '<version>' in xml_data:
            xml_data = re.sub(r'<version>[^<]*</version>', f'<version>{game_ver}</version>', xml_data)
            
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        return True
    except Exception as e:
        print_error(f"Fallo parseando {xml_path}: {e}")
        return False

def main():
    os.system("color") 
    
    # Titulo re cheto
    title = Text("Pizza-Dittos Installer Wizard", justify="center", style="bold magenta")
    console.print(Panel(title, border_style="cyan", subtitle="Preparando la magia interactiva"))
    console.print()

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
        "Che pibe, ¿donde tenes el PokeMMO?",
        choices=choices
    ).ask()

    if target == "Ingresar otra ruta manualmente":
        target = questionary.path("Pasame la ruta de PokeMMO (donde esta revision.txt):").ask()

    if not target or not os.path.exists(os.path.join(target, "revision.txt")):
        print_error("Esa ruta no tiene PokeMMO. ¡No me chamuyes!")
        sys.exit(1)

    print_success(f"Laburando en: {target}")
    
    # Obtener version
    with open(os.path.join(target, "revision.txt"), "r", encoding="utf-8-sig") as f:
        game_ver = f.read().strip()
    
    # 2. Roms (ZIP Support)
    desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    zip_files = list(desktop.glob("*okemmo*.zip")) + list(desktop.glob("*rom*.zip")) + list(desktop.glob("*.zip"))
    zip_choices = list(set([str(z) for z in zip_files]))
    
    rom_zip = questionary.select(
        "¿De donde saco las ROMs y el fondo negro modificado (patchedfile.nds)?",
        choices=zip_choices + ["Seleccionar otro ZIP", "Skipiame esto, ya tengo las ROMs puestas"]
    ).ask()
    
    if rom_zip == "Seleccionar otro ZIP":
        rom_zip = questionary.path("Pasame la ruta exacta del ZIP con las ROMs:").ask()
        
    if rom_zip and rom_zip != "Skipiame esto, ya tengo las ROMs puestas":
        print_step(f"Extrayendo ROMs desde {rom_zip}...")
        rom_dest = os.path.join(target, "roms")
        os.makedirs(rom_dest, exist_ok=True)
        
        local_roms_dir = os.path.join(base_dir, "roms")
        os.makedirs(local_roms_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(rom_zip, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if not file_info.is_dir() and file_info.filename.lower().endswith(('.nds', '.gba')):
                        file_info.filename = os.path.basename(file_info.filename)
                        if file_info.filename:
                            zip_ref.extract(file_info, local_roms_dir)
                            src_file = os.path.join(local_roms_dir, file_info.filename)
                            dst_file = os.path.join(rom_dest, file_info.filename)
                            shutil.copy2(src_file, dst_file)
            print_success("ROMs guardadas en la carpeta magica local y sincronizadas en PokeMMO.")
        except Exception as e:
            print_error(f"Hubo un re bardo extrayendo el ZIP: {e}")
            
    # 3. Theme Injection
    print_step("Inyectando el PizzaTheme...")
    theme_source = os.path.join(base_dir, "PizzaTheme")
    theme_dest = os.path.join(target, "data", "themes", "PizzaTheme")
    
    bad_mod = os.path.join(target, "data", "mods", "PizzaTheme.mod")
    bad_zip = os.path.join(target, "data", "themes", "PizzaTheme.zip")
    if os.path.exists(bad_mod): os.remove(bad_mod)
    if os.path.exists(bad_zip): os.remove(bad_zip)
    
    if os.path.exists(theme_dest):
        shutil.rmtree(theme_dest)
    shutil.copytree(theme_source, theme_dest)
    print_success("PizzaTheme inyectado. Basadisimo.")
    
    # 4. XML Version Sync Universal
    print_step(f"Sincronizando metadatos XML para PokeMMO Rev {game_ver}...")
    
    targets = [
        Path(target) / "data" / "mods",
        Path(target) / "data" / "themes"
    ]
    for d in targets:
        if d.is_dir():
            for xml_file in d.rglob("info.xml"):
                if sync_xml(xml_file, game_ver):
                    print_success(f"XML Sync: {xml_file.parent.name}")
        
    # 5. Force Theme Selection
    main_props = os.path.join(target, "config", "main.properties")
    if os.path.exists(main_props):
        with open(main_props, "r", encoding="utf-8-sig") as f:
            props = f.read()
        if 'client.ui.theme=' in props:
            props = re.sub(r'^client\.ui\.theme=.*', 'client.ui.theme=PizzaTheme', props, flags=re.MULTILINE)
        else:
            props += "\nclient.ui.theme=PizzaTheme\n"
        with open(main_props, "w", encoding="utf-8") as f:
            f.write(props)
        print_success("client.ui.theme = PizzaTheme. Forzado con exito.")

    # 6. Patcher
    print_step("Instalando el Patcher de UI...")
    patcher_dir = os.path.join(base_dir, "scripts", "patcher")
    patcher_config = os.path.join(patcher_dir, "patcher_config.json")
    
    if os.path.exists(patcher_config):
        with open(patcher_config, "r", encoding="utf-8-sig") as f:
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
    
    print_success("Patcher instalado en mods.")
    
    print_step("Ejecutando el Patcher (mod de medidas)...")
    patcher_main = os.path.join(patcher_dir, "main.py")
    try:
        subprocess.run([sys.executable, patcher_main], check=True)
        
        final_panel = Panel(
            "[bold green]¡Todo listo, pibe! El Pizza Theme y sus medidas estan de ruta.[/]\n"
            "A viciar tranquilo que el entorno quedo flama.",
            title="[bold cyan]Instalacion Completada[/]",
            border_style="green"
        )
        console.print(final_panel)
    except subprocess.CalledProcessError:
        print_error("Fallo el patcher... pego en el palo y salio.")
        
if __name__ == "__main__":
    main()
