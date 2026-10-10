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

$pokeDirs = @('C:\Program Files\PokeMMO', 'C:\PokeMMO', 'D:\PokeMMO', "$env:USERPROFILE\Desktop\PokeMMO")
$target = $null

foreach ($dir in $pokeDirs) {
    if (Test-Path (Join-Path $dir "revision.txt")) {
        $target = $dir
        break
    }
}

if (-not $target) {
    Write-Host "[!] No se encontro PokeMMO automaticamente." -ForegroundColor Yellow
    $target = Read-Host "[+] Ingresa la ruta a tu carpeta PokeMMO"
    $target = $target -replace '"', ''
}

if (-not (Test-Path (Join-Path $target "revision.txt"))) {
    Write-Host "[X] La ruta $target no parece ser una instalacion valida de PokeMMO." -ForegroundColor Red
    exit 1
}

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "[OK] Trabajando en: " -NoNewline
Write-Host $target -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

$modDestDir = Join-Path $target 'data\mods'
$badModFile = Join-Path $modDestDir 'PizzaTheme.mod'
if (Test-Path $badModFile) {
    Remove-Item -Force $badModFile
    Write-Host "[-] Basura eliminada: PizzaTheme.mod en data\mods." -ForegroundColor Yellow
}

$themeDestDir = Join-Path $target 'data\themes\PizzaTheme'
$badZipFile = Join-Path $target 'data\themes\PizzaTheme.zip'
if (Test-Path $badZipFile) {
    Remove-Item -Force $badZipFile
    Write-Host "[-] Basura eliminada: PizzaTheme.zip en data\themes." -ForegroundColor Yellow
}

$scriptPath = (Get-Location).Path
$sourceTheme = Join-Path $scriptPath "pizzatheme"

if (-not (Test-Path $sourceTheme)) {
    Write-Host "[X] No se encontro la carpeta pizzatheme en el repositorio." -ForegroundColor Red
    exit 1
}

if (Test-Path $themeDestDir) {
    Remove-Item -Recurse -Force $themeDestDir
}
New-Item -ItemType Directory -Path $themeDestDir | Out-Null
Copy-Item -Path "$sourceTheme\*" -Destination $themeDestDir -Recurse -Force
Write-Host "[OK] PizzaTheme copiado a data\themes\PizzaTheme." -ForegroundColor Green

$infoXmlPath = Join-Path $themeDestDir "info.xml"
if (Test-Path $infoXmlPath) {
    $xmlContent = Get-Content $infoXmlPath -Raw
    $xmlContent = $xmlContent -replace 'revision="[^"]*"', 'revision="8"'
    Set-Content -Path $infoXmlPath -Value $xmlContent -Encoding UTF8
    Write-Host "[OK] info.xml actualizado con revision=8." -ForegroundColor Green
}

$patcherConfigPath = Join-Path $scriptPath "scripts\patcher\patcher_config.json"
if (Test-Path $patcherConfigPath) {
    $configContent = Get-Content $patcherConfigPath -Raw | ConvertFrom-Json
    $configContent.game_path = $target
    if (-not $configContent.themes.Contains("PizzaTheme")) {
        $configContent.themes += "PizzaTheme"
    }
    $configContent | ConvertTo-Json -Depth 10 | Set-Content $patcherConfigPath -Encoding UTF8
    Write-Host "[OK] patcher_config.json actualizado con la ruta del juego." -ForegroundColor Green
}

$sourceRoms = Join-Path $scriptPath "roms"
$destRoms = Join-Path $target "roms"

if (Test-Path $sourceRoms) {
    Write-Host "-> Se detectó una carpeta local de ROMs. Preparando para transferir..." -ForegroundColor Yellow
    if (Test-Path $destRoms) {
        Write-Host "[-] Borrando ROMs antiguas en el destino..." -ForegroundColor Yellow
        Remove-Item -Path "$destRoms\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path $destRoms | Out-Null
    }
    
    Copy-Item -Path "$sourceRoms\*" -Destination $destRoms -Recurse -Force
    Write-Host "[OK] ROMs transferidas y reemplazadas exitosamente en $destRoms" -ForegroundColor Green
} else {
    Write-Host "[i] No se encontró carpeta 'roms' local. Se omite la transferencia de ROMs (Regla 18)." -ForegroundColor Cyan
}

Write-Host "-> Ejecutando el mod de las medidas (Patcher)..." -ForegroundColor Yellow
$patcherScript = Join-Path $scriptPath "scripts\patcher\main.py"
python.exe $patcherScript
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] ALERTA: Hubo un error al aplicar las medidas. Revisa los logs." -ForegroundColor Red
} else {
    Write-Host "[Exito] ¡Kanpeki! El Pizza Theme y sus medidas se han instalado y configurado de 10." -ForegroundColor Green
}

Write-Host ""
