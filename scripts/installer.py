import os
import shutil
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

def auto_sync_theme(pokemmo_dir=None):
    """
    Sincroniza la versión del info.xml del custom theme con el revision.txt del juego.
    Falla silenciosamente devolviendo False si no encuentra los archivos.
    """
    if not pokemmo_dir:
        # Rutas comunes por defecto en Windows
        common_paths = [
            "C:\\Program Files\\PokeMMO",
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

    # Extraer versión del juego usando revision.txt (la verdadera posta)
    revision_path = os.path.join(pokemmo_dir, "revision.txt")
    if not os.path.exists(revision_path):
        logger.warning("[⚠️] Auto-Sync: No se encontró revision.txt en el juego.")
        return False

    try:
        with open(revision_path, "r", encoding="utf-8") as f:
            current_version = f.read().strip()
    except Exception:
        return False

    theme_source = os.path.join(os.path.dirname(__file__), "..", "moontheme")
    theme_dest = os.path.join(pokemmo_dir, "data", "themes", "MoonTheme")
    
    # Copiar archivos si existen en source, sino, solo actualizar el dest
    try:
        if os.path.exists(theme_source) and os.path.isdir(theme_source) and len(os.listdir(theme_source)) > 1: # ignore .keep
            if os.path.exists(theme_dest):
                shutil.rmtree(theme_dest)
            shutil.copytree(theme_source, theme_dest)
    except Exception:
        pass

    # Parchear XML con la versión correcta en el destino
    moon_info_path = os.path.join(theme_dest, "info.xml")
    if os.path.exists(moon_info_path):
        try:
            tree_moon = ET.parse(moon_info_path)
            root_moon = tree_moon.getroot()
            p_version = root_moon.find("version")
            if p_version is not None:
                p_version.text = current_version
            else:
                new_v = ET.SubElement(root_moon, "version")
                new_v.text = current_version
            tree_moon.write(moon_info_path, encoding="utf-8", xml_declaration=True)
            return True
        except Exception:
            return False
    return False

def main():
    print("==============================================")
    print("✨ Instalador de Tema Moon para PokeMMO")
    print("==============================================")
    
    # Try automatic detection first
    if auto_sync_theme():
        print("\n✅ ¡Plantilla detectada e instalada automáticamente!")
    else:
        print("Arrastra la carpeta donde tienes instalado PokeMMO aqui")
        print("(ejemplo: C:\\Program Files\\PokeMMO) y presiona Enter:")
        pokemmo_dir = input("> ").strip('"').strip("'").strip()
        
        if auto_sync_theme(pokemmo_dir):
            print("\n✅ ¡Plantilla instalada y parcheada exitosamente!")
        else:
            print("\n⚠️ Ocurrió un problema instalando el tema. Revisa la ruta o permisos.")
            return

    print("1. Abre PokeMMO.")
    print("2. Ve a Ajustes -> Interfaz -> Tema y selecciona 'MoonTheme'.")
    print("3. ¡IMPORTANTE! En Ajustes -> Video, desactiva la opcion de Fondos de Combate.")

if __name__ == "__main__":
    main()
