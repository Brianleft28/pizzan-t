import os
import shutil
import xml.etree.ElementTree as ET

def main():
    print("==============================================")
    print("🎨 Instalador de Tema Pizzant para PokeMMO")
    print("==============================================")
    
    # Pedir ruta
    print("Arrastra la carpeta donde tienes instalado PokeMMO aqui")
    print("(ejemplo: C:\\PokeMMO) y presiona Enter:")
    pokemmo_dir = input("> ").strip('"').strip("'").strip()
    
    if not os.path.exists(pokemmo_dir):
        print("❌ Error: La ruta no existe.")
        return

    default_info_path = os.path.join(pokemmo_dir, "data", "themes", "default", "info.xml")
    if not os.path.exists(default_info_path):
        print("❌ Error: No se encontro el tema por defecto en PokeMMO. ¿Es la ruta correcta?")
        return

    # Extraer version del juego
    try:
        tree_default = ET.parse(default_info_path)
        root_default = tree_default.getroot()
        version_element = root_default.find("version")
        if version_element is None:
            print("❌ Error: No se pudo leer la etiqueta <version> del tema default.")
            return
        current_version = version_element.text
        print(f"✅ Version oficial de PokeMMO detectada: {current_version}")
    except Exception as e:
        print(f"❌ Error leyendo el XML original: {e}")
        return

    theme_source = os.path.join(os.path.dirname(__file__), "..", "assets", "pokemmo_theme")
    if not os.path.exists(theme_source):
        print("⚠️ Advertencia: No se encontro la carpeta assets/pokemmo_theme en el repositorio.")
        print("Asegurate de pegar los archivos de tu tema ahi antes de correr este script.")
        return

    theme_dest = os.path.join(pokemmo_dir, "data", "themes", "PizzantTheme")
    
    # Copiar archivos
    print("Copiando archivos del tema...")
    try:
        if os.path.exists(theme_dest):
            shutil.rmtree(theme_dest)
        shutil.copytree(theme_source, theme_dest)
    except Exception as e:
        print(f"❌ Error al copiar los archivos: {e}")
        return

    # Parchear XML con la version correcta
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
            print("✅ info.xml parcheado exitosamente con la nueva version.")
        except Exception as e:
            print(f"❌ Error parcheando el info.xml de PizzantTheme: {e}")
    else:
        print("⚠️ No se encontro info.xml en el tema copiado, saltando parcheo.")

    print("\n✅ ¡Plantilla instalada exitosamente!")
    print("1. Abre PokeMMO.")
    print("2. Ve a Ajustes -> Interfaz -> Tema y selecciona 'PizzantTheme'.")
    print("3. ¡IMPORTANTE! En Ajustes -> Video, desactiva la opcion de Fondos de Combate.")

if __name__ == "__main__":
    main()
