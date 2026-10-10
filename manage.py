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

console = Console()

def run_script(script_name):
    script_path = Path(__file__).parent / "scripts" / script_name
    if not script_path.exists():
        console.print(f"[bold red][ERR] No se encontró el script: {script_path}[/]")
        return
    
    try:
        subprocess.run([sys.executable, str(script_path)])
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Cancelado por el usuario.[/]")

def main():
    while True:
        console.print("\n")
        console.print(Panel("[bold cyan]Pizza-Dittos CLI Orchestrator[/bold cyan]\n[italic]Seleccioná la herramienta que querés correr:[/italic]", border_style="blue"))
        
        choices = [
            questionary.Choice("Instalador Mágico (Installer Wizard)", "installer_wizard.py"),
            questionary.Choice("Generar Release (Build Release)", "build_release.py"),
            questionary.Choice("Migrar Tema (Theme Migrator)", "theme_migrator.py"),
            questionary.Separator(),
            questionary.Choice("Salir", "exit")
        ]
        
        selection = questionary.select(
            "¿Qué hacemos, pibe?",
            choices=choices
        ).ask()
        
        if selection == "exit" or selection is None:
            console.print("[bold green]¡Nos vimos! Salu2.[/]")
            break
            
        run_script(selection)

if __name__ == "__main__":
    main()
