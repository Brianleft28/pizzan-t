import os
import shutil
import zipfile
from pathlib import Path

class ModpackExtractor:
    def __init__(self, pokemmo_client, local_roms_dir):
        self.client = pokemmo_client
        self.local_roms_dir = local_roms_dir

    def extract_zip(self, zip_path, console):
        if not os.path.exists(zip_path):
            console.print(f"[bold red][ERR] No se encontró el ZIP: {zip_path}[/]")
            return False

        rom_dest = self.client.get_roms_dir()
        mod_dest = self.client.get_mods_dir()
        theme_dest = self.client.get_themes_dir()
        
        os.makedirs(rom_dest, exist_ok=True)
        os.makedirs(mod_dest, exist_ok=True)
        os.makedirs(theme_dest, exist_ok=True)
        os.makedirs(self.local_roms_dir, exist_ok=True)

        extracted_roms = 0
        extracted_mods = 0
        extracted_themes = 0

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # 1. Identificar archivos de temas (tienen info.xml o carpetas dentro de theme/)
                # Para simplificar, si encontramos un .mod va a mods/
                # si encontramos un .nds/.gba va a roms/ y local_roms_dir
                # Para temas, extraemos la carpeta contenedora si tiene info.xml
                
                theme_roots = set()
                for file_info in zip_ref.infolist():
                    if file_info.filename.lower().endswith("info.xml"):
                        # El padre de info.xml es la raíz del tema
                        theme_roots.add(os.path.dirname(file_info.filename))
                
                for file_info in zip_ref.infolist():
                    lower_name = file_info.filename.lower()
                    
                    if lower_name.endswith(('.nds', '.gba')) and not file_info.is_dir():
                        # Extraer ROMs
                        base_name = os.path.basename(file_info.filename)
                        
                        # Extraer a local
                        local_path = os.path.join(self.local_roms_dir, base_name)
                        with zip_ref.open(file_info) as source, open(local_path, "wb") as target:
                            shutil.copyfileobj(source, target)
                            
                        # Extraer a PokeMMO
                        client_path = os.path.join(rom_dest, base_name)
                        shutil.copy2(local_path, client_path)
                        extracted_roms += 1
                        
                    elif lower_name.endswith('.mod') and not file_info.is_dir():
                        # Extraer Mods
                        base_name = os.path.basename(file_info.filename)
                        client_path = os.path.join(mod_dest, base_name)
                        with zip_ref.open(file_info) as source, open(client_path, "wb") as target:
                            shutil.copyfileobj(source, target)
                        extracted_mods += 1
                        
                    else:
                        # Extraer archivos de Temas
                        for root in theme_roots:
                            if file_info.filename.startswith(root + "/"):
                                # Mantener la estructura del tema
                                # Remover el path 'root' para que el tema quede limpio en themes/NombreTema/
                                theme_name = os.path.basename(root)
                                if not theme_name: # si el info.xml estaba en la raiz del zip
                                    theme_name = "CustomTheme"
                                    
                                rel_path = os.path.relpath(file_info.filename, root)
                                if rel_path == ".": continue
                                
                                target_path = os.path.join(theme_dest, theme_name, rel_path)
                                
                                if file_info.is_dir():
                                    os.makedirs(target_path, exist_ok=True)
                                else:
                                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                    with zip_ref.open(file_info) as source, open(target_path, "wb") as target:
                                        shutil.copyfileobj(source, target)
                                        
                                # Solo sumamos +1 por cada archivo procesado de un tema, luego lo resumimos
                                extracted_themes += 1

            console.print(f"[bold green][OK] ZIP procesado:[/]")
            console.print(f"  - ROMs extraídas: {extracted_roms}")
            console.print(f"  - Mods extraídos: {extracted_mods}")
            console.print(f"  - Archivos de Temas: {extracted_themes}")
            return True
        except Exception as e:
            console.print(f"[bold red][ERR] Falló la extracción del ZIP: {e}[/]")
            return False
