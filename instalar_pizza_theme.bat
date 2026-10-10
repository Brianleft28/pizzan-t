<# :
@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -Command "$env:BASE_ZIP='%~1'; Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw)))"
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

$baseZip = $env:BASE_ZIP
if ([string]::IsNullOrWhiteSpace($baseZip)) {
    Write-Host "[?] Se requiere el tema base para inyectar tus configuraciones." -ForegroundColor Cyan
    $baseZip = Read-Host "[+] Arrastra aca el .zip del tema base (ej. Moonlyze99.zip) y presiona Enter"
    $baseZip = $baseZip -replace '"', ''
}

if (-not (Test-Path $baseZip)) {
    Write-Host "[X] No se encontro el archivo base: $baseZip" -ForegroundColor Red
    exit 1
}

$scriptPath = (Get-Location).Path
$builderScript = Join-Path $scriptPath "scripts\build_theme_package.py"

Write-Host "-> Forjando PizzaTheme.zip desde la base..." -ForegroundColor Yellow
python.exe $builderScript "$baseZip"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] ALERTA: Hubo un error al forjar el tema. Revisa los logs." -ForegroundColor Red
    exit 1
}

$generatedZip = Join-Path $scriptPath "PizzaTheme.zip"

$pokeDirs = @('C:\Program Files\PokeMMO', 'C:\PokeMMO', 'D:\PokeMMO', "$env:USERPROFILE\Desktop\PokeMMO")
$targets = @()

foreach ($dir in $pokeDirs) {
    if (Test-Path (Join-Path $dir "revision.txt")) {
        $targets += $dir
    }
}

if ($targets.Count -eq 0) {
    Write-Host "[!] No se encontro PokeMMO automaticamente para instalarlo." -ForegroundColor Yellow
    Write-Host "[+] Tu PizzaTheme.zip esta listo en la carpeta del proyecto para instalar manualmente." -ForegroundColor Green
} else {
    foreach ($target in $targets) {
        Write-Host "==============================================" -ForegroundColor Cyan
        Write-Host "[OK] Instalando en: " -NoNewline
        Write-Host $target -ForegroundColor Cyan
        Write-Host "==============================================" -ForegroundColor Cyan
        
        $modDestDir = Join-Path $target 'data\mods'
        $badModFile = Join-Path $modDestDir 'PizzaTheme.mod'
        if (Test-Path $badModFile) {
            Remove-Item -Force $badModFile
            Write-Host "[-] Se elimino el viejo PizzaTheme.mod defectuoso." -ForegroundColor Yellow
        }

        $themeDestDir = Join-Path $target 'data\themes'
        if (-not (Test-Path $themeDestDir)) {
            New-Item -ItemType Directory -Path $themeDestDir | Out-Null
        }
        
        $finalThemeZip = Join-Path $themeDestDir 'PizzaTheme.zip'
        Copy-Item -Path $generatedZip -Destination $finalThemeZip -Force
        Write-Host "[OK] PizzaTheme.zip instalado exitosamente en $themeDestDir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "[Exito] El Pizza Theme ha sido actualizado y empaquetado." -ForegroundColor Green
Write-Host ""
