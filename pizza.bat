@echo off
title Pizza-Dittos Orchestrator

IF NOT EXIST ".\venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual (venv).
    echo Por favor, lee el README.md y ejecuta "python -m venv venv" y "pip install -r requirements.txt" primero.
    pause
    exit /b
)

.\venv\Scripts\python.exe manage.py
pause
