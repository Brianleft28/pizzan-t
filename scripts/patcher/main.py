"""
main.py - PokeMMO UI Patcher (modo automatico).

Lee patcher_config.json, aplica los parches a los XML y listo.
Sin preguntas, sin CLI interactivo. Ejecutar y olvidarse.

Uso:
    python main.py              Aplica los parches configurados
    python main.py --restore    Restaura los valores por defecto del juego
    python main.py --init       Genera patcher_config.json con valores recomendados
"""

from __future__ import annotations

import sys
from pathlib import Path

from config import (
    PATCH_TARGETS,
    load_config,
    save_config,
    resolve_theme_path,
    DEFAULT_CONFIG,
    CONFIG_FILE,
)
from xml_engine import apply_patch, restore_defaults, read_current_values
from backup import create_backup

# ---------------------------------------------------------------------------
# Utilidades de consola
# ---------------------------------------------------------------------------

SEPARATOR = "-" * 55

# Colores ANSI (funcionan en Windows 10+ y terminales modernas)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def ok(msg: str):
    print(f"  {GREEN}[OK]{RESET} {msg}")


def warn(msg: str):
    print(f"  {YELLOW}[!!]{RESET} {msg}")


def err(msg: str):
    print(f"  {RED}[ERR]{RESET} {msg}")


def info(msg: str):
    print(f"  {CYAN}[..]{RESET} {msg}")


def header(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {BOLD}{title}{RESET}")
    print(SEPARATOR)


# ---------------------------------------------------------------------------
# Flujo de parcheo automatico
# ---------------------------------------------------------------------------

def run_patch(config: dict):
    """Aplica todos los parches habilitados en la configuracion."""
    game_path = Path(config["game_path"])
    themes = config.get("themes", ["default"])
    patches = config.get("patches", {})

    if not game_path.is_dir():
        err(f"Game path not found: {game_path}")
        err("Edit 'game_path' in patcher_config.json with the correct path.")
        return False

    success_count = 0
    error_count = 0

    for theme_name in themes:
        header(f"Theme: {theme_name}")

        try:
            theme_path = resolve_theme_path(game_path, theme_name)
        except FileNotFoundError as e:
            err(str(e))
            error_count += 1
            continue

        info(f"Directorio: {theme_path}")

        for target_key, patch_cfg in patches.items():
            if not patch_cfg.get("enabled", True):
                continue

            target = PATCH_TARGETS.get(target_key)
            if target is None:
                warn(f"Unknown target in config: '{target_key}' (skipped)")
                continue

            xml_path = theme_path / target.xml_file

            if not xml_path.exists():
                warn(f"{target.label}: file not found ({target.xml_file})")
                continue

            # Extraer los valores a aplicar (excluir "enabled")
            new_values = {
                k: str(v) for k, v in patch_cfg.items()
                if k != "enabled" and k in [p.name for p in target.params]
            }

            if not new_values:
                continue

            # Leer valores actuales para comparar
            current = read_current_values(xml_path, target)
            already_patched = all(
                current.get(k) == v for k, v in new_values.items()
            )

            if already_patched:
                ok(f"{target.label}: already has the correct values")
                success_count += 1
                continue

            # Crear backup y aplicar
            try:
                backup_file = create_backup(xml_path)
                changes = apply_patch(xml_path, target, new_values)
                ok(f"{target.label}: patched")
                for pname, change in changes.items():
                    print(f"        {pname}: {change['old']} -> {change['new']}")
                success_count += 1
            except Exception as e:
                err(f"{target.label}: {e}")
                error_count += 1

    return error_count == 0


# ---------------------------------------------------------------------------
# Flujo de restauracion
# ---------------------------------------------------------------------------

def run_restore(config: dict):
    """Restaura todos los targets a sus valores por defecto del juego."""
    game_path = Path(config["game_path"])
    themes = config.get("themes", ["default"])
    patches = config.get("patches", {})

    if not game_path.is_dir():
        err(f"Game path not found: {game_path}")
        return False

    for theme_name in themes:
        header(f"Restoring theme: {theme_name}")

        try:
            theme_path = resolve_theme_path(game_path, theme_name)
        except FileNotFoundError as e:
            err(str(e))
            continue

        for target_key in patches:
            target = PATCH_TARGETS.get(target_key)
            if target is None:
                continue

            xml_path = theme_path / target.xml_file
            if not xml_path.exists():
                continue

            try:
                create_backup(xml_path)
                changes = restore_defaults(xml_path, target)
                ok(f"{target.label}: restored to default values")
                for pname, change in changes.items():
                    print(f"        {pname}: {change['old']} -> {change['new']}")
            except Exception as e:
                err(f"{target.label}: {e}")

    return True


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    # Habilitar colores ANSI en Windows
    try:
        import os
        os.system("")
    except Exception:
        pass

    print(f"\n{'=' * 55}")
    print(f"  {BOLD}PokeMMO UI Patcher v1.0{RESET}")
    print(f"  Customize the size of your game windows")
    print(f"{'=' * 55}")

    config_path = Path(__file__).parent / CONFIG_FILE

    # Manejar argumentos de linea de comandos
    args = sys.argv[1:]

    if "--init" in args:
        save_config(DEFAULT_CONFIG, config_path)
        ok(f"Config created: {config_path}")
        info("Edit patcher_config.json with your values and run again.")
        return

    # Cargar configuracion (la crea si no existe)
    config = load_config(config_path)

    if "--restore" in args:
        header("RESTORE MODE")
        run_restore(config)
    else:
        run_patch(config)

    header("DONE")
    print()


if __name__ == "__main__":
    main()
