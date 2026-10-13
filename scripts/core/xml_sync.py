import re
import xml.etree.ElementTree as ET


def sync_xml(xml_path, game_ver):
    """
    Lee un archivo info.xml y actualiza los tags 'revision' y 'version' para que PokeMMO lo acepte.
    Solo toca atributos DENTRO de <theme> y <resource>, nunca la declaracion <?xml ...?>.
    Si el resultado no es XML valido, no escribe nada.
    """
    try:
        with open(xml_path, "r", encoding="utf-8-sig") as f:
            xml_data = f.read()

        # Reparar declaraciones rotas por la version anterior de este script (<?xml version="8" ...?>)
        xml_data = re.sub(r'(<\?xml\s+)version="[^"]*"', r'\1version="1.0"', xml_data, count=1)

        # Sincronizar theme revision="8" (solo dentro del tag <theme>)
        if re.search(r'<theme\b[^>]*\brevision="', xml_data):
            xml_data = re.sub(r'(<theme\b[^>]*?\b)revision="[^"]*"', r'\1revision="8"', xml_data)
        elif '<theme' in xml_data:
            xml_data = re.sub(r'<theme\b', '<theme revision="8"', xml_data, count=1)

        # Sincronizar resource version="8" para mods (solo dentro del tag <resource>)
        if re.search(r'<resource\b[^>]*\bversion="', xml_data):
            xml_data = re.sub(r'(<resource\b[^>]*?\b)version="[^"]*"', r'\1version="8"', xml_data)
        elif '<resource' in xml_data:
            xml_data = re.sub(r'<resource\b', '<resource version="8"', xml_data, count=1)

        # Sincronizar la etiqueta <version> (para temas y mods viejos)
        if '<version>' in xml_data:
            xml_data = re.sub(r'<version>[^<]*</version>', f'<version>{game_ver}</version>', xml_data)

        # Validar antes de escribir: si quedo roto, no tocamos el archivo
        ET.fromstring(xml_data.encode("utf-8"))

        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_data)
        return True
    except Exception:
        return False
