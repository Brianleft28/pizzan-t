"""
theme_migrator.py - Migrador de PizzaTheme para PokeMMO.

Copia los XMLs actualizados del tema default del juego al PizzaTheme,
preservando los assets visuales custom (res/, textures/, fonts/) y
actualizando info.xml para que el juego acepte el mod.

Uso:
    python scripts/theme_migrator.py              # Ejecutar migración
    python scripts/theme_migrator.py --dry-run    # Solo mostrar cambios sin escribir
"""

from __future__ import annotations

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

GAME_PATH = Path(r"C:\Program Files\PokeMMO")
DEFAULT_THEME = GAME_PATH / "data" / "themes" / "default"
PIZZA_MOD = GAME_PATH / "data" / "mods" / "PizzaTheme"
PIZZA_THEME_DIR = PIZZA_MOD / "Moonlyze99"
BACKUP_SUFFIX = f".pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"

# Colores ANSI
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# XMLs del sistema de UI que deben sincronizarse con el default actual.
# Estos archivos definen la ESTRUCTURA de la interfaz (nodos, layouts, widgets).
# Si están desactualizados, el juego rechaza el tema o crashea al renderizar.
SYNC_XMLS = [
    # Raíz del tema
    "theme.xml",
    "init.xml",
    "gfx.xml",
    "gfx_ui.xml",
    "fonts.xml",
    "cursors.xml",
    "main-widgets.xml",
    "twl-themer-load.xml",
    # Subdirectorio ui/
    "ui/battle.xml",
    "ui/main.xml",
    "ui/inventory.xml",
    "ui/chat.xml",
    "ui/contest.xml",
    "ui/party.xml",
    "ui/monster-dex.xml",
    "ui/monster-frame.xml",
    "ui/customization.xml",
    "ui/settings.xml",
    "ui/guild.xml",
    "ui/matchmaking.xml",
    "ui/social.xml",
    "ui/instance.xml",
    "ui/tt.xml",
    "ui/trade.xml",
    "ui/shop.xml",
    "ui/link.xml",
    "ui/misc.xml",
    "ui/advanced-search.xml",
    "ui/broker.xml",
    "ui/pc.xml",
    "ui/incubator.xml",
    "ui/staff.xml",
]

# Directorios con assets VISUALES del PizzaTheme que NO se deben tocar.
# Estos son los PNG, TTF y texturas que hacen que el tema se vea como Pizza.
PRESERVE_DIRS = ["res", "textures", "Fancy", "atlas"]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def ok(msg: str):
    print(f"  {GREEN}[OK]{RESET} {msg}")

def warn(msg: str):
    print(f"  {YELLOW}[!!]{RESET} {msg}")

def err(msg: str):
    print(f"  {RED}[ERR]{RESET} {msg}")

def info(msg: str):
    print(f"  {CYAN}[..]{RESET} {msg}")

def header(title: str):
    sep = "-" * 55
    print(f"\n{sep}")
    print(f"  {BOLD}{title}{RESET}")
    print(sep)


# ---------------------------------------------------------------------------
# Paso 1: Backup de seguridad
# ---------------------------------------------------------------------------

def backup_pizza_theme(dry_run: bool):
    """Crea un backup completo del PizzaTheme antes de tocarlo."""
    backup_dir = PIZZA_MOD.parent / f"PizzaTheme_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if dry_run:
        info(f"[DRY-RUN] Backup se crearía en: {backup_dir}")
        return
    
    info(f"Creando backup completo en: {backup_dir}")
    shutil.copytree(PIZZA_MOD, backup_dir)
    ok(f"Backup creado: {backup_dir}")


# ---------------------------------------------------------------------------
# Paso 2: Sincronizar XMLs del default → PizzaTheme
# ---------------------------------------------------------------------------

def sync_xmls(dry_run: bool):
    """Copia los XMLs actualizados del default al PizzaTheme."""
    header("SINCRONIZACIÓN DE XMLs")
    
    synced = 0
    skipped = 0
    
    for xml_rel in SYNC_XMLS:
        src = DEFAULT_THEME / xml_rel
        dst = PIZZA_THEME_DIR / xml_rel
        
        if not src.exists():
            warn(f"No existe en default: {xml_rel}")
            skipped += 1
            continue
        
        # Comparar tamaños/fechas para ver si realmente necesita actualización
        needs_update = True
        if dst.exists():
            if src.stat().st_size == dst.stat().st_size:
                # Comparación rápida por contenido
                if src.read_bytes() == dst.read_bytes():
                    needs_update = False
        
        if not needs_update:
            ok(f"Ya actualizado: {xml_rel}")
            skipped += 1
            continue
        
        if dry_run:
            size_src = src.stat().st_size
            size_dst = dst.stat().st_size if dst.exists() else 0
            info(f"[DRY-RUN] Actualizaría: {xml_rel} ({size_dst}B → {size_src}B)")
            synced += 1
            continue
        
        # Backup individual del XML viejo
        if dst.exists():
            bak = dst.with_suffix(dst.suffix + BACKUP_SUFFIX)
            shutil.copy2(dst, bak)
        
        # Asegurar que el directorio padre exista
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # Copiar el XML actualizado
        shutil.copy2(src, dst)
        ok(f"Actualizado: {xml_rel}")
        synced += 1
    
    info(f"Resultado: {synced} actualizados, {skipped} sin cambios")
    return synced


# ---------------------------------------------------------------------------
# Paso 3: Actualizar info.xml con el formato correcto
# ---------------------------------------------------------------------------

NEW_INFO_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<resource name="Moonlyze99" version="5" description="Moonlyze99 Theme Version Pizza (Migrated)" author="Moonlyze99" weblink="https://forums.pokemmo.com/index.php?/topic/188683-moonlyze99-theme-pc-%F0%9F%8D%90/">
    <themes theme_revision="8">
        <theme path="Moonlyze99" name="PizzaTheme" is_mobile="false"/>
    </themes>
</resource>
"""


def update_info_xml(dry_run: bool):
    """Reescribe info.xml con el formato que espera la versión actual del juego."""
    header("ACTUALIZACIÓN DE info.xml")
    
    info_path = PIZZA_MOD / "info.xml"
    
    if dry_run:
        info("[DRY-RUN] Se reescribiría info.xml con formato theme_revision")
        print(f"\n{CYAN}--- Contenido nuevo ---{RESET}")
        print(NEW_INFO_XML)
        return
    
    # Backup
    if info_path.exists():
        bak = info_path.with_suffix(info_path.suffix + BACKUP_SUFFIX)
        shutil.copy2(info_path, bak)
        ok(f"Backup de info.xml original: {bak.name}")
    
    info_path.write_text(NEW_INFO_XML, encoding="utf-8")
    ok("info.xml actualizado con theme_revision=\"8\"")


# ---------------------------------------------------------------------------
# Paso 4: Verificar integridad
# ---------------------------------------------------------------------------

def verify_integrity():
    """Verifica que todos los archivos críticos existan tras la migración."""
    header("VERIFICACIÓN DE INTEGRIDAD")
    
    errors = 0
    
    # Verificar info.xml
    info_path = PIZZA_MOD / "info.xml"
    if not info_path.exists():
        err("info.xml NO EXISTE")
        errors += 1
    else:
        content = info_path.read_text(encoding="utf-8")
        if 'theme_revision="8"' in content:
            ok("info.xml: theme_revision=\"8\" presente ✓")
        else:
            err("info.xml: falta theme_revision")
            errors += 1
    
    # Verificar XMLs críticos
    critical = ["theme.xml", "init.xml", "gfx.xml", "main-widgets.xml"]
    for xml_name in critical:
        path = PIZZA_THEME_DIR / xml_name
        if path.exists():
            ok(f"{xml_name}: existe ({path.stat().st_size} bytes) ✓")
        else:
            err(f"{xml_name}: NO ENCONTRADO")
            errors += 1
    
    # Verificar que los assets visuales se preservaron
    for dir_name in PRESERVE_DIRS:
        dir_path = PIZZA_THEME_DIR / dir_name
        if dir_path.exists() and dir_path.is_dir():
            count = sum(1 for _ in dir_path.rglob("*") if _.is_file())
            ok(f"{dir_name}/: {count} assets preservados ✓")
        else:
            if dir_name == "atlas":
                info(f"{dir_name}/: no existe (opcional)")
            else:
                warn(f"{dir_name}/: directorio no encontrado")
    
    if errors == 0:
        print(f"\n  {GREEN}{BOLD}✅ MIGRACIÓN EXITOSA - El tema debería cargar en el juego{RESET}")
    else:
        print(f"\n  {RED}{BOLD}❌ {errors} ERRORES DETECTADOS - Revisar manualmente{RESET}")
    
    return errors


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    # Habilitar colores ANSI en Windows
    try:
        os.system("")
    except Exception:
        pass

    dry_run = "--dry-run" in sys.argv

    print(f"\n{'=' * 55}")
    print(f"  {BOLD}PizzaTheme Migrator v1.0{RESET}")
    print(f"  Sincroniza XMLs del default actual al PizzaTheme")
    print(f"{'=' * 55}")
    
    if dry_run:
        print(f"\n  {YELLOW}⚠️  MODO DRY-RUN: No se escribirán cambios{RESET}\n")

    # Validaciones
    if not GAME_PATH.is_dir():
        err(f"No se encontró PokeMMO en: {GAME_PATH}")
        return 1
    
    if not DEFAULT_THEME.is_dir():
        err(f"No se encontró el tema default en: {DEFAULT_THEME}")
        return 1
    
    if not PIZZA_THEME_DIR.is_dir():
        err(f"No se encontró PizzaTheme en: {PIZZA_THEME_DIR}")
        return 1

    # Ejecutar pasos
    backup_pizza_theme(dry_run)
    sync_xmls(dry_run)
    update_info_xml(dry_run)
    
    if not dry_run:
        errors = verify_integrity()
        return errors
    else:
        header("DRY-RUN COMPLETO")
        info("Ejecuta sin --dry-run para aplicar los cambios.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
