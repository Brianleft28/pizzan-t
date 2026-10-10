@echo off
title PokeMMO UI Patcher
echo.
echo   Applying UI patches...
echo.

:: Look for Python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0main.py" %*
    goto :end
)

:: Try py launcher (Windows)
where py >nul 2>&1
if %errorlevel% equ 0 (
    py "%~dp0main.py" %*
    goto :end
)

echo   [ERR] Python not found.
echo   Download it at: https://www.python.org/downloads/
echo.

:end
pause
