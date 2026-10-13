@echo off
title PizzaHunter Orchestrator
cd /d "%~dp0"

IF NOT EXIST "venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual - carpeta venv.
    echo Por favor, lee el README.md y ejecuta "python -m venv venv" y "pip install -r requirements.txt" primero.
    pause
    exit /b
)

"venv\Scripts\python.exe" manage.py
pause
