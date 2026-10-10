@echo off
chcp 65001 >nul
echo [?] Preparando entorno para el pibe...

if not exist venv (
    echo [??] Creando entorno virtual (venv)...
    python -m venv venv
)

call venv\Scripts\activate.bat
echo [??] Instalando dependencias necesarias (cero complacencia)...
pip install -q questionary

echo [??] Lanzando el wizard interactivo...
python scripts\installer_wizard.py

pause
