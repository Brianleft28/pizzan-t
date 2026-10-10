@echo off
TITLE Importar Cerebro PizzaHunter
echo [1/2] Restaurando cerebro de PizzaHunter en esta PC...
if not exist "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1\" mkdir "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1\"
xcopy ".\.pizzahunter\*" "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1\" /E /I /H /Y
echo [2/2] Completado. Ahora podes abrir la extension y buscar el chat en el historial.
pause
