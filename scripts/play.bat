@echo off
TITLE Pizzant - The Humanoid Hunter
COLOR 0B

echo ==============================================
echo  INICIANDO REGLAS DE PLAY (PIZZANT)
echo ==============================================

:: Forzar codificacion UTF-8
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

:: Activar entorno virtual
echo [1/2] Activando entorno virtual...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No se encontro la carpeta 'venv'. Asegurate de estar en la carpeta correcta.
    pause
    exit /b
)

:: Iniciar Bot
echo [2/2] Levantando Pizzant (main_gui.py)...
python main_gui.py

pause
