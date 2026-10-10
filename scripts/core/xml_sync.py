import re

def sync_xml(xml_path, game_ver):
    """
    Lee un archivo info.xml y actualiza los tags 'revision' y 'version' para que PokeMMO lo acepte.
    """
    try:
        with open(xml_path, "r", encoding="utf-8-sig") as f:
            xml_data = f.read()
            
        # Sincronizar theme revision="8"
        if '<theme' in xml_data and 'revision="' not in xml_data:
            xml_data = re.sub(r'<theme([^>]*)>', r'<theme revision="8"\1>', xml_data)
        elif '<theme' in xml_data:
            xml_data = re.sub(r'revision="[^"]*"', 'revision="8"', xml_data)
            
        # Sincronizar resource version="8" para mods
        if '<resource' in xml_data and 'version="' not in xml_data:
            xml_data = re.sub(r'<resource([^>]*)>', r'<resource version="8"\1>', xml_data)
        elif '<resource' in xml_data:
            xml_data = re.sub(r'version="[^"]*"', 'version="8"', xml_data)
            
        # Sincronizar la etiqueta <version> (para temas y mods viejos)
        if '<version>' in xml_data:
            xml_data = re.sub(r'<version>[^<]*</version>', f'<version>{game_ver}</version>', xml_data)
            
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        return True
    except Exception as e:
        return False
