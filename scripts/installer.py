import os
import shutil
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

def auto_sync_theme(pokemmo_dir=None):
    """
    Sincroniza la versión del info.xml del juego con el custom theme de Pizzant.
    Si pokemmo_dir no se proporciona, intenta buscar en ubicaciones comunes.
    Falla silenciosamente devolviendo False si no puede hacerlo.
    """
    if not pokemmo_dir:
        # Rutas comunes por defecto en Windows
        common_paths = [
            "C:\\PokeMMO",
            "D:\\PokeMMO",
            os.path.expanduser("~\\Desktop\\PokeMMO")
        ]
        for path in common_paths:
            if os.path.exists(path):
                pokemmo_dir = path
                break
        
    if not pokemmo_dir or not os.path.exists(pokemmo_dir):
        logger.warning("[⚠️] Auto-Sync: Directorio PokeMMO no encontrado. Saltando parcheo.")
        return False

    default_info_path = os.path.join(pokemmo_dir, "data", "themes", "default", "info.xml")
    if not os.path.exists(default_info_path):
        logger.warning("[⚠️] Auto-Sync: No se encontró el info.xml del tema default.")
        return False

    # Extraer versión del juego
    try:
        tree_default = ET.parse(default_info_path)
        root_default = tree_default.getroot()
        version_element = root_default.find("version")
        if version_element is None:
            return False
        current_version = version_element.text
    except Exception:
        return False

    theme_source = os.path.join(os.path.dirname(__file__), "..", "assets", "pokemmo_theme")
    theme_dest = os.path.join(pokemmo_dir, "data", "themes", "PizzantTheme")
    
    # Copiar archivos si existen en source, sino, solo actualizar el dest
    try:
        if os.path.exists(theme_source) and os.path.isdir(theme_source) and len(os.listdir(theme_source)) > 1: # ignore .keep
            if os.path.exists(theme_dest):
                shutil.rmtree(theme_dest)
            shutil.copytree(theme_source, theme_dest)
    except Exception:
        pass

    # Parchear XML con la versión correcta en el destino
    pizzant_info_path = os.path.join(theme_dest, "info.xml")
    if os.path.exists(pizzant_info_path):
        try:
            tree_pizzant = ET.parse(pizzant_info_path)
            root_pizzant = tree_pizzant.getroot()
            p_version = root_pizzant.find("version")
            if p_version is not None:
                p_version.text = current_version
            else:
                new_v = ET.SubElement(root_pizzant, "version")
                new_v.text = current_version
            tree_pizzant.write(pizzant_info_path, encoding="utf-8", xml_declaration=True)
            return True
        except Exception:
            return False
    return False

def main():
    print("==============================================")
    print("✨ Instalador de Tema Pizzant para PokeMMO")
    print("==============================================")
    
    print("Arrastra la carpeta donde tienes instalado PokeMMO aqui")
    print("(ejemplo: C:\\PokeMMO) y presiona Enter:")
    pokemmo_dir = input("> ").strip('"').strip("'").strip()
    
    if auto_sync_theme(pokemmo_dir):
        print("\n✅ ¡Plantilla instalada y parcheada exitosamente!")
        print("1. Abre PokeMMO.")
        print("2. Ve a Ajustes -> Interfaz -> Tema y selecciona 'PizzantTheme'.")
        print("3. ¡IMPORTANTE! En Ajustes -> Video, desactiva la opcion de Fondos de Combate.")
    else:
        print("\n⚠️ Ocurrió un problema instalando el tema. Revisa la ruta o permisos.")

if __name__ == "__main__":
    main()
