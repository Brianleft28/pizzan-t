"""
config.py - Definiciones de targets parcheables para PokeMMO UI Patcher.

Cada target describe:
  - El archivo XML relativo a la raiz del tema.
  - La ruta jerarquica de nodos <theme name="..."> hasta el nodo objetivo.
  - Los parametros que se pueden modificar (minWidth, minHeight, maxHeight, etc.).
  - Los valores por defecto del juego (para restauracion).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Resolucion de rutas de tema
# ---------------------------------------------------------------------------

DEFAULT_THEME_REL = Path("data", "themes", "default")
MODS_BASE_REL = Path("data", "mods")


def resolve_theme_path(game_path: Path, theme_name: str) -> Path:
    """Resuelve la ruta del directorio del tema.

    Args:
        game_path: Ruta raiz de instalacion de PokeMMO.
        theme_name: "default" para el tema base, o el nombre del
                    mod/tema custom (ej: "Moonlyze99").

    Returns:
        Ruta absoluta al directorio que contiene theme.xml y los XMLs de UI.
    """
    if theme_name.lower() == "default":
        return game_path / DEFAULT_THEME_REL

    # Tema custom: data/mods/<nombre>/<nombre>/
    mod_dir = game_path / MODS_BASE_REL / theme_name
    if not mod_dir.is_dir():
        raise FileNotFoundError(f"Mod no encontrado: {mod_dir}")

    # Buscar subdirectorio con theme.xml
    for sub in mod_dir.iterdir():
        if sub.is_dir() and (sub / "theme.xml").exists():
            return sub

    raise FileNotFoundError(
        f"No se encontro theme.xml dentro de {mod_dir}"
    )


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PatchParam:
    """Un parametro individual modificable dentro de un nodo XML."""
    name: str          # Nombre del <param name="...">
    tag: str           # Tipo de valor: "int", "dimension", etc.
    default: str       # Valor por defecto original del juego


@dataclass
class PatchTarget:
    """Un elemento de la UI que puede ser parcheado."""
    label: str                        # Nombre legible
    xml_file: str                     # Ruta relativa al tema
    theme_path: list[str]             # Jerarquia de theme[@name]
    params: list[PatchParam]          # Parametros modificables
    description: str = ""


# ---------------------------------------------------------------------------
# Registro de targets parcheables
# ---------------------------------------------------------------------------

PATCH_TARGETS: dict[str, PatchTarget] = {

    "inventory": PatchTarget(
        label="Inventario",
        xml_file="ui/inventory.xml",
        theme_path=[
            "inventory-tabbedframe",
            "dialoglayout",
            "tabbedpane",
        ],
        params=[
            PatchParam("minWidth",  "int", "530"),
            PatchParam("minHeight", "int", "378"),
        ],
        description="Tamano minimo de la ventana de inventario.",
    ),

    "mods_panel": PatchTarget(
        label="Panel de Mods",
        xml_file="ui/settings.xml",
        theme_path=[
            "mods-panel",
        ],
        params=[
            PatchParam("minHeight", "int", "300"),
        ],
        description="Alto minimo del panel de gestion de mods.",
    ),

    "encounter_frame": PatchTarget(
        label="Frame del Encounter Counter",
        xml_file="main-widgets.xml",
        theme_path=[
            "encounter-counter-frame",
        ],
        params=[
            PatchParam("minWidth",  "int", "540"),
            PatchParam("maxHeight", "int", "340"),
        ],
        description="Tamano del frame principal del contador de encuentros.",
    ),

    "encounter_history_scroll": PatchTarget(
        label="Scrollpane del Historial Shiny",
        xml_file="main-widgets.xml",
        theme_path=[
            "encounter-counter-frame",
            "tabbedpane",
            "container",
            "encounter-counter-history",
            "scrollpane",
        ],
        params=[
            PatchParam("minHeight", "int", "260"),
        ],
        description="Alto del area de scroll del historial de encuentros shiny.",
    ),

    "encounter_summary_scroll": PatchTarget(
        label="Scrollpane del Resumen de Encuentros",
        xml_file="main-widgets.xml",
        theme_path=[
            "encounter-counter-frame",
            "tabbedpane",
            "container",
            "encounter-counter-summary",
            "scrollpane",
        ],
        params=[
            PatchParam("minHeight", "int", "260"),
        ],
        description="Alto del area de scroll del resumen de encuentros.",
    ),
}


# ---------------------------------------------------------------------------
# Lectura del archivo de configuracion del usuario
# ---------------------------------------------------------------------------

CONFIG_FILE = "patcher_config.json"

DEFAULT_CONFIG = {
    "game_path": "C:\\Program Files\\PokeMMO",
    "themes": ["default"],
    "patches": {
        "inventory": {
            "enabled": True,
            "minWidth": 530,
            "minHeight": 567,
        },
        "mods_panel": {
            "enabled": True,
            "minHeight": 1000,
        },
        "encounter_frame": {
            "enabled": True,
            "minWidth": 540,
            "maxHeight": 600,
        },
        "encounter_history_scroll": {
            "enabled": True,
            "minHeight": 420,
        },
        "encounter_summary_scroll": {
            "enabled": True,
            "minHeight": 420,
        },
    },
}


def load_config(config_path: Path | None = None) -> dict:
    """Carga la configuracion del usuario desde patcher_config.json.

    Si el archivo no existe, lo crea con valores recomendados por defecto
    y retorna esos valores.
    """
    if config_path is None:
        config_path = Path(__file__).parent / CONFIG_FILE

    if not config_path.exists():
        save_config(DEFAULT_CONFIG, config_path)
        return DEFAULT_CONFIG

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config: dict, config_path: Path | None = None):
    """Guarda la configuracion en formato JSON legible."""
    if config_path is None:
        config_path = Path(__file__).parent / CONFIG_FILE

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
