@echo off
TITLE Exportar Cerebro PizzaHunter
echo [1/3] Exportando cerebro de la IA (Chat actual)...
xcopy "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1" ".\.pizzahunter\" /E /I /H /Y
echo [2/3] Subiendo a GitHub...
git add -f .pizzahunter
git commit -m "chore: backup de conversacion de la IA (PizzaHunter)"
git push origin main
echo [3/3] Listo. Ya podes ir a la otra PC y ejecutar import_pizzahunter.bat
pause
