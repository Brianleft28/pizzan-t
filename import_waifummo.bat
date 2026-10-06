@echo off
TITLE Importar Cerebro WaifuMMO
echo [1/2] Restaurando cerebro de WaifuMMO en esta PC...
xcopy ".\.waifummo" "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1\" /E /I /H /Y
echo [2/2] Completado. Ahora podes abrir la extension y buscar el chat en el historial.
pause
