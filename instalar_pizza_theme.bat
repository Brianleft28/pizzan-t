<# :
@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw)))"
pause
exit /b
#>
$ErrorActionPreference = 'Stop'

Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host " [☁️] Aplicando Regla del Pull: Actualizando repositorio..." -ForegroundColor Cyan
git pull origin main
Write-Host "==============================================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "   ____    ___  ____  _____ _   _ " -ForegroundColor Magenta
Write-Host "  / ___|  / _ \|  _ \| ____| \ | |" -ForegroundColor Magenta
Write-Host "  \___ \ | | | | |_) |  _| |  \| |" -ForegroundColor Cyan
Write-Host "   ___) || |_| |  _ <| |___| |\  |" -ForegroundColor Cyan
Write-Host "  |____/  \___/|_| \_\_____|_| \_|" -ForegroundColor Green
Write-Host "  >> INICIANDO PROTOCOLO PIZZANT v7.0 <<" -ForegroundColor Magenta
Write-Host "==============================================================" -ForegroundColor DarkGray
Write-Host ""

Write-Host " [⚠️] RECORDATORIO CRITICO (REGLA 18)" -ForegroundColor Red
Write-Host " El bot necesita ROMs de Black/White modificadas (sin fondos)." -ForegroundColor Red
Write-Host " Si no las tenes, yo me encargo de bajarlas mágicamente." -ForegroundColor Red
Write-Host "==============================================================" -ForegroundColor DarkGray
Write-Host ""
Read-Host " [💖] Presiona ENTER para desatar la magia, bebito..." | Out-Null
Write-Host ""

$scriptPath = (Get-Location).Path
$sourceTheme = Join-Path $scriptPath "pizzatheme"

if (-not (Test-Path $sourceTheme)) {
    Write-Host "[X] No se encontro la carpeta pizzatheme. Rompiste algo." -ForegroundColor Red
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
    Write-Host "[!] No encontre PokeMMO. ¿Donde lo escondiste?" -ForegroundColor Yellow
    $target = Read-Host "[+] Ingresa la ruta a tu carpeta PokeMMO"
    $target = $target -replace '"', ''
}

if (-not (Test-Path (Join-Path $target "revision.txt"))) {
    Write-Host "[X] Che, esa ruta no es de PokeMMO. Cancelando operacion." -ForegroundColor Red
    exit 1
}

Write-Host "==============================================" -ForegroundColor Magenta
Write-Host "[OK] Trabajando en: " -NoNewline
Write-Host $target -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Magenta
Write-Host ""
Read-Host " [✨] Presiona ENTER para inyectar el tema visual..." | Out-Null

# Autenticando version (Opcion B)
$gameRevisionPath = Join-Path $target "revision.txt"
$gameVer = (Get-Content $gameRevisionPath -Raw).Trim()

$miInfoPath = Join-Path $sourceTheme "info.xml"
if (Test-Path $miInfoPath) {
    Write-Host " [⚙️] Sincronizando version del tema con la del juego ($gameVer)..." -ForegroundColor Yellow
    $miXml = Get-Content $miInfoPath -Raw
    
    if ($miXml -notmatch 'revision="') {
        $miXml = $miXml -replace '<theme([^>]*)>', "<theme revision=""8""`$1>"
    }
    
    $miXml = $miXml -replace '<version>[^<]*</version>', "<version>$gameVer</version>"
    Set-Content -Path $miInfoPath -Value $miXml -Encoding UTF8
    Write-Host " [OK] PizzaTheme actualizado para soportar la version $gameVer" -ForegroundColor Green
}

$modDestDir = Join-Path $target 'data\mods'
$badModFile = Join-Path $modDestDir 'PizzaTheme.mod'
if (Test-Path $badModFile) {
    Remove-Item -Force $badModFile
    Write-Host " [🗑️] Basura eliminada: PizzaTheme.mod en data\mods." -ForegroundColor DarkYellow
}

$themeDestDir = Join-Path $target 'data\themes\PizzaTheme'
$badZipFile = Join-Path $target 'data\themes\PizzaTheme.zip'
if (Test-Path $badZipFile) {
    Remove-Item -Force $badZipFile
    Write-Host " [🗑️] Basura eliminada: PizzaTheme.zip en data\themes." -ForegroundColor DarkYellow
}

if (Test-Path $themeDestDir) {
    Remove-Item -Recurse -Force $themeDestDir
}
New-Item -ItemType Directory -Path $themeDestDir | Out-Null
Copy-Item -Path "$sourceTheme\*" -Destination $themeDestDir -Recurse -Force
Write-Host " [OK] PizzaTheme inyectado 完璧 (Kanpeki) en data\themes." -ForegroundColor Green

$mainPropsPath = Join-Path $target "config\main.properties"
if (Test-Path $mainPropsPath) {
    Write-Host " [🔧] Forzando seleccin de PizzaTheme en main.properties..." -ForegroundColor Yellow
    $props = Get-Content $mainPropsPath
    $props = $props -replace '^client\.ui\.theme=.*', 'client.ui.theme=PizzaTheme'
    $props | Set-Content $mainPropsPath -Encoding UTF8
    Write-Host " [OK] client.ui.theme = PizzaTheme. ¡0 complacencia, yo decido!" -ForegroundColor Green
}

$patcherConfigPath = Join-Path $scriptPath "scripts\patcher\patcher_config.json"
if (Test-Path $patcherConfigPath) {
    $configContent = Get-Content $patcherConfigPath -Raw | ConvertFrom-Json
    $configContent.game_path = $target
    if (-not $configContent.themes.Contains("PizzaTheme")) {
        $configContent.themes += "PizzaTheme"
    }
    $configContent | ConvertTo-Json -Depth 10 | Set-Content $patcherConfigPath -Encoding UTF8
    Write-Host " [OK] Config del patcher sincronizada." -ForegroundColor Green
}

Write-Host ""
Read-Host " [🎮] Presiona ENTER para procesar las ROMs..." | Out-Null

$sourceRoms = Join-Path $scriptPath "roms"
$destRoms = Join-Path $target "roms"

if (-not (Test-Path $sourceRoms)) {
    New-Item -ItemType Directory -Path $sourceRoms | Out-Null
}

$ndsFiles = Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse -ErrorAction SilentlyContinue
if (-not $ndsFiles) {
    Write-Host " [☁️] Carpeta local 'roms' vacia. Bajando de Drive (cero complacencia)..." -ForegroundColor Yellow
    $driveId = "1GkVzxranBiYRV47jBCiCH0IakpOBlpwx"
    $url = "https://drive.google.com/uc?export=download&id=$driveId"
    $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
    
    $warningPage = Invoke-RestMethod -Uri $url -WebSession $session -ErrorAction SilentlyContinue
    if ($warningPage -match 'name="uuid" value="([^"]+)"') {
        $uuid = $Matches[1]
        Write-Host "   [🕵️] Archivo >100MB detectado. Bypasseando barrera de Google..." -ForegroundColor Cyan
        $dlUrl = "https://drive.usercontent.google.com/download?id=$driveId&export=download&confirm=t&uuid=$uuid"
        Invoke-WebRequest -Uri $dlUrl -WebSession $session -OutFile "temp_roms.zip"
        
        Write-Host "   [📦] Extrayendo magia en tu entorno local..." -ForegroundColor Cyan
        Expand-Archive -Path "temp_roms.zip" -DestinationPath $sourceRoms -Force
        Remove-Item -Force "temp_roms.zip"
        
        Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse | Where-Object { $_.DirectoryName -ne $sourceRoms } | ForEach-Object {
            Move-Item -Path $_.FullName -Destination $sourceRoms -Force
        }
        Get-ChildItem -Path $sourceRoms -Directory -Recurse | Remove-Item -Recurse -Force
        
        Write-Host "   [OK] ROMs descargadas y preparadas." -ForegroundColor Green
    } else {
        Write-Host "   [X] Fallo de red. Ponelas a mano, bebito." -ForegroundColor Red
    }
}

if (Get-ChildItem -Path $sourceRoms -Filter "*.nds" -Recurse -ErrorAction SilentlyContinue) {
    Write-Host " [⚙️] ROMs detectadas. Sincronizando con PokeMMO..." -ForegroundColor Yellow
    if (Test-Path $destRoms) {
        Write-Host "   [☠️] Destruyendo ROMs viejas en el juego..." -ForegroundColor DarkYellow
        Remove-Item -Path "$destRoms\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        New-Item -ItemType Directory -Path $destRoms | Out-Null
    }
    
    Copy-Item -Path "$sourceRoms\*" -Destination $destRoms -Recurse -Force
    Write-Host "   [💖] ROMs inyectadas exitosamente." -ForegroundColor Green
} else {
    Write-Host " [i] No se obtuvieron ROMs. El bot se quedara ciego." -ForegroundColor DarkGray
}

Write-Host ""
Read-Host " [🖌️] Presiona ENTER para aplicar el Patcher de UI..." | Out-Null

Write-Host " [🔥] Ejecutando el mod de las medidas (Patcher)..." -ForegroundColor Magenta
$patcherScript = Join-Path $scriptPath "scripts\patcher\main.py"
python.exe $patcherScript
if ($LASTEXITCODE -ne 0) {
    Write-Host " [X] ALERTA: Fallo en el Patcher. Revisa si falta Python." -ForegroundColor Red
} else {
    Write-Host " [💖] ¡Kanpeki! El Pizza Theme y sus medidas estan god. A viciar, pibe." -ForegroundColor Green
}

Write-Host ""
