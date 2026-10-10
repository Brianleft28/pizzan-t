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

$scriptPath = (Get-Location).Path
$sourceTheme = Join-Path $scriptPath "pizzatheme"

if (-not (Test-Path $sourceTheme)) {
    Write-Host "[X] No se encontro la carpeta pizzatheme en el repositorio." -ForegroundColor Red
    exit 1
}

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

# Autenticando version (Opcion B)
$gameRevisionPath = Join-Path $target "revision.txt"
$gameVer = (Get-Content $gameRevisionPath -Raw).Trim()

$miInfoPath = Join-Path $sourceTheme "info.xml"
if (Test-Path $miInfoPath) {
    Write-Host "-> Sincronizando version del tema con la version del juego ($gameVer)..." -ForegroundColor Yellow
    $miXml = Get-Content $miInfoPath -Raw
    
    # Inyectar revision 8 por defecto si no existe, o mantener la que haya
    if ($miXml -notmatch 'revision="') {
        $miXml = $miXml -replace '<theme([^>]*)>', "<theme revision=""8""`$1>"
    }
    
    $miXml = $miXml -replace '<version>[^<]*</version>', "<version>$gameVer</version>"
    Set-Content -Path $miInfoPath -Value $miXml -Encoding UTF8
    Write-Host "[OK] Tu carpeta pizzatheme fue actualizada para soportar la version $gameVer" -ForegroundColor Green
}

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

if (Test-Path $themeDestDir) {
    Remove-Item -Recurse -Force $themeDestDir
}
New-Item -ItemType Directory -Path $themeDestDir | Out-Null
Copy-Item -Path "$sourceTheme\*" -Destination $themeDestDir -Recurse -Force
Write-Host "[OK] PizzaTheme copiado a data\themes\PizzaTheme." -ForegroundColor Green

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

if (-not (Test-Path $sourceRoms)) {
    New-Item -ItemType Directory -Path $sourceRoms | Out-Null
}

$ndsFiles = Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse -ErrorAction SilentlyContinue
if (-not $ndsFiles) {
    Write-Host "-> La carpeta local 'roms' esta vacia. Descargando desde Google Drive (cero complacencia)..." -ForegroundColor Yellow
    $driveId = "1GkVzxranBiYRV47jBCiCH0IakpOBlpwx"
    $url = "https://drive.google.com/uc?export=download&id=$driveId"
    $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
    
    $warningPage = Invoke-RestMethod -Uri $url -WebSession $session -ErrorAction SilentlyContinue
    if ($warningPage -match 'name="uuid" value="([^"]+)"') {
        $uuid = $Matches[1]
        Write-Host "   [i] Archivo >100MB detectado. Bypasseando barrera de virus de Google..." -ForegroundColor Cyan
        $dlUrl = "https://drive.usercontent.google.com/download?id=$driveId&export=download&confirm=t&uuid=$uuid"
        Invoke-WebRequest -Uri $dlUrl -WebSession $session -OutFile "temp_roms.zip"
        
        Write-Host "   [i] Extrayendo ROMs al entorno local..." -ForegroundColor Cyan
        Expand-Archive -Path "temp_roms.zip" -DestinationPath $sourceRoms -Force
        Remove-Item -Force "temp_roms.zip"
        
        # Aplanar (mover todo a la raiz de roms/ y borrar subcarpetas)
        Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse | Where-Object { $_.DirectoryName -ne $sourceRoms } | ForEach-Object {
            Move-Item -Path $_.FullName -Destination $sourceRoms -Force
        }
        Get-ChildItem -Path $sourceRoms -Directory -Recurse | Remove-Item -Recurse -Force
        
        Write-Host "   [OK] ROMs preparadas en la carpeta local del repo." -ForegroundColor Green
    } else {
        Write-Host "   [!] Error de red al bajar el ZIP. Pon las ROMs manualmente en roms/." -ForegroundColor Red
    }
}

if (Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse -ErrorAction SilentlyContinue) {
    Write-Host "-> Se detectaron ROMs locales. Sincronizando con PokeMMO..." -ForegroundColor Yellow
    if (Test-Path $destRoms) {
        Write-Host "   [-] Borrando ROMs antiguas en el juego..." -ForegroundColor Yellow
        Remove-Item -Path "$destRoms\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path $destRoms | Out-Null
    }
    
    Copy-Item -Path "$sourceRoms\*" -Destination $destRoms -Recurse -Force
    Write-Host "   [OK] ROMs transferidas y reemplazadas exitosamente en $destRoms" -ForegroundColor Green
} else {
    Write-Host "[i] No se obtuvieron ROMs. El bot OCR podria fallar (Regla 18)." -ForegroundColor Cyan
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
