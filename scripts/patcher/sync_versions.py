import xml.etree.ElementTree as ET
from pathlib import Path
import sys

def sync_xml_version(xml_path: Path, new_version: str="8", new_revision: str="8"):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        modified = False
        
        # 1. Modificar atributo de <resource> (usado por Mods)
        if root.tag == "resource":
            if root.get("version") != new_version:
                root.set("version", new_version)
                modified = True
                
        # 2. Modificar atributo de <theme> (usado por Temas)
        if root.tag == "theme":
            if root.get("revision") != new_revision:
                root.set("revision", new_revision)
                modified = True
                
        # 3. Buscar subnodos <theme> dentro de un <resource>
        for theme_node in root.findall(".//theme"):
            if theme_node.get("revision") != new_revision:
                theme_node.set("revision", new_revision)
                modified = True
                
        if modified:
            tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
            print(f" [OK] Sincronizado correctamente: {xml_path}")
    except Exception as e:
        print(f" [ERR] Fallo parseando {xml_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python sync_versions.py <ruta_pokemmo>")
        sys.exit(1)
        
    base_dir = Path(sys.argv[1])
    
    if not base_dir.is_dir():
        print(f" [ERR] Directorio no encontrado: {base_dir}")
        sys.exit(1)
        
    print(f" [**] Buscando info.xml recursivamente en: {base_dir} ...")
    
    # Buscar todos los info.xml en data/mods y data/themes
    targets = [
        base_dir / "data" / "mods",
        base_dir / "data" / "themes"
    ]
    
    found_any = False
    for target_dir in targets:
        if target_dir.is_dir():
            for xml_file in target_dir.rglob("info.xml"):
                found_any = True
                sync_xml_version(xml_file)
                
    if not found_any:
        print(" [i] No se encontro ningun info.xml para sincronizar.")

if __name__ == "__main__":
    main()
