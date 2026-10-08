"""
theme_migrator.py - Migrador de PizzaTheme para PokeMMO.

Copia los XMLs actualizados del tema default del juego a nuestra carpeta pizzatheme local,
preservando los assets visuales custom (textures/, icon.png) y omitiendo info.xml
para no pisar nuestra metadata.
"""

import os
import sys
import shutil
from pathlib import Path

# Configuraciones
WORKSPACE_DIR = Path(__file__).resolve().parent.parent
PIZZA_THEME_DIR = WORKSPACE_DIR / "pizzatheme"
DEFAULT_GAME_PATHS = [
    Path(r"C:\Program Files\PokeMMO"),
    Path(r"C:\PokeMMO"),
    Path(r"D:\PokeMMO"),
    Path.home() / "Desktop" / "PokeMMO"
]

def find_pokemmo():
    for p in DEFAULT_GAME_PATHS:
        if (p / "data" / "themes" / "default").exists():
            return p
    return None

def main():
    print("=" * 55)
    print("  PizzaTheme Migrator (Full Scrape)")
    print("=" * 55)

    game_path = find_pokemmo()
    if not game_path:
        print("[!] No se encontro la carpeta PokeMMO con el tema default.")
        sys.exit(1)

    default_theme_dir = game_path / "data" / "themes" / "default"
    print(f"[OK] Encontrado PokeMMO default theme en: {default_theme_dir}")

    if not PIZZA_THEME_DIR.exists():
        PIZZA_THEME_DIR.mkdir(parents=True)
        print(f"[OK] Creada carpeta local: {PIZZA_THEME_DIR}")

    # Archivos que queremos saltarnos
    SKIP_FILES = ["info.xml"]

    print("\n[..] Copiando XMLs exhaustivamente...")
    count = 0
    # Recorrer todo el default_theme_dir
    for root, dirs, files in os.walk(default_theme_dir):
        for file in files:
            if file.endswith(".xml") and file not in SKIP_FILES:
                src_file = Path(root) / file
                rel_path = src_file.relative_to(default_theme_dir)
                dest_file = PIZZA_THEME_DIR / rel_path
                
                # Crear carpetas necesarias en el destino
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(src_file, dest_file)
                count += 1
                
    print(f"[OK] Copiados {count} archivos XML al repositorio local.")
    print("\n[OK] Migracion completa. Ahora podes correr instalar_mods_y_tema.bat para probar.")

if __name__ == "__main__":
    main()
