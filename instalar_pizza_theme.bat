<# :
@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw)))"
pause
exit /b
#>
$ErrorActionPreference = 'Stop'

Write-Host "  _____ _                  _______ _                          " -ForegroundColor Yellow
Write-Host " |  __ (_)                |__   __| |                         " -ForegroundColor Yellow
Write-Host " | |__) | __________ _       | |  | |__   ___ _ __ ___   ___  " -ForegroundColor Yellow
Write-Host " |  ___/ |___  /_  / _\      | |  | '_ \ / _ \ '_ \ _ \ / _ \ " -ForegroundColor Yellow
Write-Host " | |   | |  / / / / (_| |    | |  | | | |  __/ | | | | |  __/ " -ForegroundColor Yellow
Write-Host " |_|   |_| /___/___\__,_|    |_|  |_| |_|\___|_| |_| |_|\___| " -ForegroundColor Yellow
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "==============================================================" -ForegroundColor Red
Write-Host " [WARNING] RECORDATORIO CRITICO SOBRE LAS ROMS (REGLA 18)" -ForegroundColor Red
Write-Host " El bot necesita ROMs de Black/White modificadas (sin fondos)." -ForegroundColor Red
Write-Host " Estas ROMs NO se suben a Git por peso/copyright." -ForegroundColor Red
Write-Host " Si estas en una PC nueva, transferilas MANUALMENTE a la" -ForegroundColor Red
Write-Host " carpeta roms/ de tu PokeMMO o el OCR no va a cazar una." -ForegroundColor Red
Write-Host "==============================================================" -ForegroundColor Red
Write-Host ""
Write-Host ""

$pokeDirs = @('C:\Program Files\PokeMMO', 'C:\PokeMMO', 'D:\PokeMMO', "$env:USERPROFILE\Desktop\PokeMMO")
$targets = @()

foreach ($dir in $pokeDirs) {
    if (Test-Path (Join-Path $dir "revision.txt")) {
        $targets += $dir
    }
}

if ($targets.Count -eq 0) {
    Write-Host "[X] No se pudo encontrar PokeMMO automaticamente." -ForegroundColor Red
    $manualTarget = Read-Host "[+] Por favor, arrastra aca la carpeta de PokeMMO (y presiona Enter)"
    $manualTarget = $manualTarget -replace '"', ''
    if (Test-Path (Join-Path $manualTarget "revision.txt")) {
        $targets += $manualTarget
    } else {
        Write-Host "[X] Ruta invalida. No se encontro revision.txt en: $manualTarget" -ForegroundColor Red
        exit 1
    }
}

$scriptPath = (Get-Location).Path

foreach ($target in $targets) {
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "[OK] Instalando en: " -NoNewline
    Write-Host $target -ForegroundColor Cyan
    Write-Host "==============================================" -ForegroundColor Cyan
    
    Write-Host "-> Limpiando instalacion antigua del tema (Legacy)..." -ForegroundColor Yellow
    $legacyThemeDest = Join-Path $target 'data\themes\pizzatheme'
    if (Test-Path $legacyThemeDest) {
        Remove-Item -Recurse -Force $legacyThemeDest
        Write-Host "[OK] Carpeta antigua en data\themes\pizzatheme eliminada." -ForegroundColor Green
    }

    Write-Host "-> Construyendo e Instalando Pizza Theme (Mod format)..." -ForegroundColor Yellow
    Write-Host -NoNewline "[" -ForegroundColor Cyan
    for ($i = 0; $i -lt 30; $i++) {
        Write-Host -NoNewline "█" -ForegroundColor Green
        Start-Sleep -Milliseconds 40
    }
    Write-Host "] Completado!" -ForegroundColor Cyan
    $modDestDir = Join-Path $target 'data\mods'
    if (-not (Test-Path $modDestDir)) {
        New-Item -ItemType Directory -Path $modDestDir | Out-Null
    }
    
    $modThemeFile = Join-Path $modDestDir 'PizzaTheme.mod'
    $pythonPath = "python"
    $buildScript = Join-Path $scriptPath "scripts\build_mod.py"
    
    if (Test-Path $buildScript) {
        & $pythonPath $buildScript $modThemeFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] PizzaTheme.mod compilado exitosamente en $modDestDir" -ForegroundColor Green
        } else {
            Write-Host "[!] Hubo un error al compilar PizzaTheme.mod." -ForegroundColor Red
        }
    } else {
        Write-Host "[!] No se encontro el script de construccion scripts\build_mod.py" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "[Exito] El Pizza Theme ha sido actualizado." -ForegroundColor Green
Write-Host ""
