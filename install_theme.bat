@echo off
chcp 65001 >nul
echo Iniciando Instalador de Interfaz Pizzant...
if exist "..\venv\Scripts\activate" (
    call "..\venv\Scripts\activate"
) else if exist ".\venv\Scripts\activate" (
    call ".\venv\Scripts\activate"
) else (
    echo ⚠️ Advertencia: Entorno virtual no encontrado, intentando usar Python global...
)

if exist "scripts\installer.py" (
    python scripts\installer.py
) else if exist "installer.py" (
    python installer.py
) else (
    echo ❌ Error: No se encuentra installer.py. Ejecuta el archivo desde la raiz del proyecto.
)
pause
