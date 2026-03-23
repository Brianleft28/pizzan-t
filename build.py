import PyInstaller.__main__
import os
import customtkinter
import sys

# Buscamos la ruta real de customtkinter en tu sistema
ctk_path = os.path.dirname(customtkinter.__file__)

def build():
    print(f"Buscando customtkinter en: {ctk_path}")
    print("Iniciando compilación... Esto puede tardar un toque porque easyocr es pesado.")
    
    PyInstaller.__main__.run([
        'main_gui.py',
        '--name=ShinyHunter',
        '--onefile', # Todo en un solo archivo
        '--windowed', # Sin consola negra de fondo
        # Incluimos los scripts necesarios
        '--add-data=selector.py;.',
        '--add-data=src;src',
        # El truco para que customtkinter no tire error:
        f'--add-data={ctk_path};customtkinter/',
        # Forzamos los imports
        '--hidden-import=customtkinter',
        '--hidden-import=cv2',
        '--hidden-import=mss',
        '--hidden-import=easyocr',
        '--hidden-import=requests',
        '--hidden-import=PIL',
        '--icon=NONE'
    ])

    print("\n¡Listo el pollo! Fijate en la carpeta /dist, ahí tenés el ShinyHunter.exe")

if __name__ == "__main__":
    build()
