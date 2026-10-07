@echo off
chcp 65001 >nul
echo Iniciando Instalador Definitivo...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\install.ps1"
pause
