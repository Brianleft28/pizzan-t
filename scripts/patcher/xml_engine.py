"""
xml_engine.py - Motor de parseo y modificacion segura de XML para PokeMMO.

Estrategia de busqueda:
  Se navega el arbol XML siguiendo la jerarquia de theme[@name] definida en
  config.PatchTarget.theme_path.  No depende de numeros de linea; funciona
  aunque los parches del juego reordenen o agreguen nodos.

Se usa xml.etree.ElementTree con preservacion de declaracion XML, comentarios
y formato general del archivo original.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from config import PatchTarget, PatchParam


# ---------------------------------------------------------------------------
# Busqueda jerarquica de nodos <theme>
# ---------------------------------------------------------------------------

def _find_theme_child(parent: ET.Element, theme_name: str) -> Optional[ET.Element]:
    """Busca un hijo directo o anidado <theme name='theme_name'> dentro de parent.

    Primero busca entre hijos directos; si no lo encuentra, hace una busqueda
    recursiva (BFS) para cubrir casos donde el nodo esta envuelto en capas
    intermedias.
    """
    # Busqueda directa entre hijos
    for child in parent:
        if child.tag == "theme" and child.get("name") == theme_name:
            return child

    # Busqueda recursiva (BFS) si no se encontro como hijo directo
    queue = list(parent)
    while queue:
        node = queue.pop(0)
        for child in node:
            if child.tag == "theme" and child.get("name") == theme_name:
                return child
            queue.append(child)

    return None


def find_target_node(root: ET.Element, theme_path: list[str]) -> Optional[ET.Element]:
    """Navega la jerarquia de theme_path partiendo desde root.

    Args:
        root: Elemento raiz del XML (normalmente <themes>).
        theme_path: Lista ordenada de valores name= por los que navegar.

    Returns:
        El elemento <theme> final, o None si algun eslabon no se encontro.
    """
    current = root
    for name in theme_path:
        found = _find_theme_child(current, name)
        if found is None:
            return None
        current = found
    return current


# ---------------------------------------------------------------------------
# Lectura y escritura de parametros
# ---------------------------------------------------------------------------

def get_param_value(node: ET.Element, param_name: str) -> Optional[str]:
    """Lee el valor actual de un <param name='param_name'> dentro de node."""
    for param in node:
        if param.tag == "param" and param.get("name") == param_name:
            # El valor esta dentro de un sub-elemento como <int>, <dimension>, etc.
            value_elem = next(iter(param), None)
            if value_elem is not None and value_elem.text:
                return value_elem.text.strip()
            # Fallback: texto directo
            if param.text and param.text.strip():
                return param.text.strip()
    return None


def set_param_value(node: ET.Element, param_name: str, value: str,
                    value_tag: str = "int") -> bool:
    """Establece el valor de un <param name='param_name'> existente.

    Si el parametro no existe, lo crea como nuevo hijo del nodo.

    Args:
        node: Nodo <theme> que contiene el parametro.
        param_name: Nombre del parametro (atributo name=).
        value: Nuevo valor a establecer.
        value_tag: Tag del sub-elemento (ej: "int", "dimension").

    Returns:
        True si se modifico o creo exitosamente.
    """
    for param in node:
        if param.tag == "param" and param.get("name") == param_name:
            value_elem = next(iter(param), None)
            if value_elem is not None:
                value_elem.text = value
            else:
                # Re-crear sub-elemento
                param.clear()
                param.set("name", param_name)
                sub = ET.SubElement(param, value_tag)
                sub.text = value
            return True

    # El parametro no existe: crearlo
    new_param = ET.SubElement(node, "param")
    new_param.set("name", param_name)
    sub = ET.SubElement(new_param, value_tag)
    sub.text = value
    return True


# ---------------------------------------------------------------------------
# Operacion completa de parcheo
# ---------------------------------------------------------------------------

def apply_patch(xml_path: Path, target: PatchTarget,
                new_values: dict[str, str]) -> dict[str, dict]:
    """Aplica un parche a un archivo XML.

    Args:
        xml_path: Ruta absoluta al archivo XML.
        target: Definicion del target a parchear.
        new_values: Diccionario {param_name: nuevo_valor}.

    Returns:
        Diccionario con los cambios realizados:
        {param_name: {"old": valor_anterior, "new": valor_nuevo}}

    Raises:
        FileNotFoundError: Si el archivo XML no existe.
        ValueError: Si no se encuentra el nodo objetivo en el XML.
    """
    if not xml_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    node = find_target_node(root, target.theme_path)
    if node is None:
        raise ValueError(
            f"No se encontro el nodo objetivo siguiendo la ruta: "
            f"{' > '.join(target.theme_path)}\n"
            f"en el archivo: {xml_path}"
        )

    changes: dict[str, dict] = {}

    for param_name, new_value in new_values.items():
        # Encontrar la definicion del param en el target
        param_def = next(
            (p for p in target.params if p.name == param_name), None
        )
        if param_def is None:
            continue

        old_value = get_param_value(node, param_name)
        set_param_value(node, param_name, new_value, param_def.tag)
        changes[param_name] = {"old": old_value or "N/A", "new": new_value}

    # Escribir con declaracion XML y codificacion correcta
    tree.write(xml_path, encoding="UTF-8", xml_declaration=True)

    return changes


def restore_defaults(xml_path: Path, target: PatchTarget) -> dict[str, dict]:
    """Restaura los valores por defecto de un target.

    Args:
        xml_path: Ruta al archivo XML.
        target: Definicion del target con los valores default.

    Returns:
        Diccionario con los cambios realizados.
    """
    defaults = {p.name: p.default for p in target.params}
    return apply_patch(xml_path, target, defaults)


def read_current_values(xml_path: Path, target: PatchTarget) -> dict[str, str]:
    """Lee los valores actuales de todos los parametros de un target.

    Returns:
        Diccionario {param_name: valor_actual}.
    """
    if not xml_path.exists():
        return {}

    tree = ET.parse(xml_path)
    root = tree.getroot()
    node = find_target_node(root, target.theme_path)

    if node is None:
        return {}

    result: dict[str, str] = {}
    for param_def in target.params:
        val = get_param_value(node, param_def.name)
        result[param_def.name] = val or param_def.default
    return result
