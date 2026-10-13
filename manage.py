import os
import sys
import subprocess
from pathlib import Path

try:
    import questionary
except ImportError:
    print("Falta questionary. Ejecutá: pip install questionary")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print("Falta rich. Ejecutá: pip install rich")
    sys.exit(1)

# Importar core classes
sys.path.append(str(Path(__file__).parent))
from scripts.core.pokemmo import PokeMMOClient
from scripts.core.extractor import ModpackExtractor
from scripts.core.xml_sync import sync_xml

console = Console()
base_dir = Path(__file__).parent.absolute()

def _get_client():
    client = PokeMMOClient()
    if not client.auto_detect():
        target = questionary.path("No se encontró PokeMMO. Pasame la ruta exacta:").ask()
        if not client.set_target(target):
            console.print("[bold red][ERR] Ruta inválida.[/]")
            return None
    return client

def install_roms_and_mods(client=None):
    client = client or _get_client()
    if not client: return

    desktop = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    zip_files = list(desktop.glob("*okemmo*.zip")) + list(desktop.glob("*rom*.zip")) + list(desktop.glob("*.zip"))
    zip_choices = list(set([str(z) for z in zip_files])) + ["Ingresar otra ruta"]
    
    rom_zip = questionary.select("Seleccioná el ZIP con las ROMs/Mods/Temas:", choices=zip_choices).ask()
    if rom_zip == "Ingresar otra ruta":
        rom_zip = questionary.path("Ruta del ZIP:").ask()
        
    if rom_zip:
        local_roms_dir = os.path.join(base_dir, "roms")
        extractor = ModpackExtractor(client, local_roms_dir)
        console.print("[bold yellow][..] Extrayendo archivos mágicamente...[/]")
        extractor.extract_zip(rom_zip, console)

def install_pizza_theme(client=None):
    client = client or _get_client()
    if not client: return

    import shutil
    theme_source = os.path.join(base_dir, "PizzaTheme")
    if not os.path.exists(theme_source):
        theme_source = os.path.join(base_dir, "pizzatheme")
    theme_dest = os.path.join(client.get_themes_dir(), "PizzaTheme")
    
    if os.path.exists(theme_dest):
        shutil.rmtree(theme_dest)
    shutil.copytree(theme_source, theme_dest)
    
    client.force_theme("PizzaTheme")
    console.print("[bold green][OK] PizzaTheme inyectado y forzado correctamente.[/]")

def sync_xml_versions(client=None):
    client = client or _get_client()
    if not client: return
    
    console.print(f"[bold yellow][..] Sincronizando metadatos XML para PokeMMO Rev {client.game_ver}...[/]")
    targets = [Path(client.get_mods_dir()), Path(client.get_themes_dir())]
    for d in targets:
        if d.is_dir():
            for xml_file in d.rglob("info.xml"):
                if sync_xml(xml_file, client.game_ver):
                    console.print(f"  [bold green][OK] Sincronizado: {xml_file.parent.name}[/]")

def run_ui_patcher(client=None):
    client = client or _get_client()
    if client:
        patcher_config_file = os.path.join(base_dir, "scripts", "patcher", "patcher_config.json")
        if os.path.exists(patcher_config_file):
            try:
                import json
                with open(patcher_config_file, "r", encoding="utf-8-sig") as f:
                    pcfg = json.load(f)
                pcfg["game_path"] = client.target_dir
                if "PizzaTheme" not in pcfg.get("themes", []):
                    pcfg.setdefault("themes", []).append("PizzaTheme")
                with open(patcher_config_file, "w", encoding="utf-8") as f:
                    json.dump(pcfg, f, indent=4)
            except Exception as e:
                console.print(f"[bold yellow][!] Aviso: No se pudo actualizar patcher_config.json: {e}[/]")

    patcher_main = os.path.join(base_dir, "scripts", "patcher", "main.py")
    if not os.path.exists(patcher_main):
        console.print("[bold red][ERR] No se encontró el patcher.[/]")
        return
    try:
        subprocess.run([sys.executable, patcher_main])
    except KeyboardInterrupt:
        pass

def full_guided_install():
    console.print(Panel("[bold green]Instalador Completo PizzaHunter (Todo en Uno)[/bold green]\n"
                        "[white]Ejecutando detección, ROMs/Mods, PizzaTheme, Sync XML y Patcher...[/white]",
                        border_style="green"))
    client = _get_client()
    if not client: return

    console.print("\n[bold cyan]Paso 1: Extracción de ROMs y Mods[/bold cyan]")
    install_roms_and_mods(client)
    console.print("\n[bold cyan]Paso 2: Instalación de PizzaTheme[/bold cyan]")
    install_pizza_theme(client)
    console.print("\n[bold cyan]Paso 3: Sincronización XML[/bold cyan]")
    sync_xml_versions(client)
    console.print("\n[bold cyan]Paso 4: Patcher de Medidas de UI[/bold cyan]")
    run_ui_patcher(client)

    console.print(Panel("[bold green]¡Instalación completa finalizada con éxito![/bold green]\n"
                        "[cyan]Ya podés abrir PokeMMO y arrancar el bot (Opción 4).[/cyan]",
                        border_style="green"))

def run_bot():
    bot_main = os.path.join(base_dir, "main_gui.py")
    if not os.path.exists(bot_main):
        console.print("[bold red][ERR] No se encontró el bot (main_gui.py).[/]")
        return
    console.print("[bold green][..] Arrancando PizzaHunter Bot...[/]")
    try:
        subprocess.run([sys.executable, bot_main])
    except KeyboardInterrupt:
        pass

def main():
    os.system("color")
    while True:
        console.print("\n")
        console.print(Panel("[bold cyan]PizzaHunter CLI Orchestrator[/bold cyan]\n[italic]Seleccioná la herramienta que querés correr:[/italic]", border_style="blue"))
        
        choices = [
            questionary.Choice("0. Instalación Completa Guiada (Todo en Uno)", "full_install"),
            questionary.Choice("1. Extraer ZIP de ROMs y Mods al juego", "extract_zip"),
            questionary.Choice("2. Instalar PizzaTheme", "install_pizza"),
            questionary.Choice("3. Modificar medidas de UI (Patcher)", "run_patcher"),
            questionary.Choice("4. Arrancar el Bot (main_gui.py)", "run_bot"),
            questionary.Choice("5. Sincronizar versiones XML de todos los temas/mods", "sync_xml"),
            questionary.Separator(),
            questionary.Choice("Ejecutar Build Release", "build_release"),
            questionary.Choice("Migrar Tema Antiguo", "theme_migrator"),
            questionary.Separator(),
            questionary.Choice("Salir", "exit")
        ]
        
        selection = questionary.select("¿Qué hacemos, pibe?", choices=choices).ask()
        
        if selection == "exit" or selection is None:
            console.print("[bold green]¡Nos vimos! Salu2.[/]")
            break
        elif selection == "full_install":
            full_guided_install()
        elif selection == "extract_zip":
            install_roms_and_mods()
        elif selection == "install_pizza":
            install_pizza_theme()
        elif selection == "run_patcher":
            run_ui_patcher()
        elif selection == "run_bot":
            run_bot()
        elif selection == "sync_xml":
            sync_xml_versions()
        elif selection == "build_release":
            subprocess.run([sys.executable, str(base_dir / "scripts" / "build_release.py")])
        elif selection == "theme_migrator":
            subprocess.run([sys.executable, str(base_dir / "scripts" / "theme_migrator.py")])

if __name__ == "__main__":
    main()
