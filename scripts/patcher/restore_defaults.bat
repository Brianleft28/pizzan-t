@echo off
title PokeMMO UI Patcher - Restore
echo.
echo   Restoring default values...
echo.

where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0main.py" --restore
    goto :end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py "%~dp0main.py" --restore
    goto :end
)

echo   [ERR] Python not found.

:end
pause
