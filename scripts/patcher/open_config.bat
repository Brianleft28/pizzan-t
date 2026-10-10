@echo off
title PokeMMO UI Patcher - Configuration
echo.
echo   Opening configuration window...
echo.

where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0config_gui.py"
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py "%~dp0config_gui.py"
    goto :end
)

echo   [ERR] Python not found.
echo   Download it at: https://www.python.org/downloads/

:end
pause
