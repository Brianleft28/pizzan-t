<# :
@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw -Encoding UTF8))) -ArgumentList '%~dp0'"
pause
exit /b
#>
param($passedPath)
Write-Host "Passed path: $passedPath"

