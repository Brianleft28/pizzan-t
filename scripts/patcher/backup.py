"""
backup.py - Sistema de backup y restauracion de archivos XML.

Genera copias de seguridad con timestamp antes de cada modificacion.
Permite restaurar desde el backup mas reciente o uno especifico.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

BACKUP_DIR_NAME = ".pokemmo_patcher_backups"


def _get_backup_dir(xml_path: Path) -> Path:
    """Obtiene (y crea si no existe) el directorio de backups junto al XML."""
    backup_dir = xml_path.parent / BACKUP_DIR_NAME
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def _backup_name(xml_path: Path, timestamp: str) -> str:
    """Genera un nombre de backup: original_name.YYYYMMDD_HHMMSS.bak"""
    return f"{xml_path.name}.{timestamp}.bak"


def create_backup(xml_path: Path) -> Path:
    """Crea un backup del archivo XML actual.

    Args:
        xml_path: Ruta absoluta al archivo XML original.

    Returns:
        Ruta al archivo de backup creado.

    Raises:
        FileNotFoundError: Si el archivo original no existe.
    """
    if not xml_path.exists():
        raise FileNotFoundError(f"No se puede respaldar: {xml_path} no existe.")

    backup_dir = _get_backup_dir(xml_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / _backup_name(xml_path, timestamp)

    shutil.copy2(xml_path, backup_file)
    return backup_file


def list_backups(xml_path: Path) -> list[Path]:
    """Lista todos los backups disponibles para un archivo XML, ordenados por fecha.

    Returns:
        Lista de rutas a backups, del mas reciente al mas antiguo.
    """
    backup_dir = xml_path.parent / BACKUP_DIR_NAME
    if not backup_dir.exists():
        return []

    pattern = f"{xml_path.name}.*.bak"
    backups = sorted(backup_dir.glob(pattern), reverse=True)
    return backups


def restore_latest_backup(xml_path: Path) -> Path | None:
    """Restaura el backup mas reciente de un archivo XML.

    Returns:
        Ruta al backup usado, o None si no hay backups disponibles.
    """
    backups = list_backups(xml_path)
    if not backups:
        return None

    latest = backups[0]
    shutil.copy2(latest, xml_path)
    return latest


def restore_specific_backup(xml_path: Path, backup_path: Path) -> bool:
    """Restaura desde un backup especifico.

    Returns:
        True si la restauracion fue exitosa.
    """
    if not backup_path.exists():
        return False

    shutil.copy2(backup_path, xml_path)
    return True
