<# :
@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw)))"
pause
exit /b
#>
$ErrorActionPreference = 'Stop'

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   Instalador Definitivo: Mods y Pizza Theme     " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
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
    
    $revPath = Join-Path $target "revision.txt"
    $revision = Get-Content $revPath -Raw
    $revision = $revision.Trim()

    Write-Host "-> Limpiando instalacion antigua del tema (Legacy)..." -ForegroundColor Yellow
    $legacyThemeDest = Join-Path $target 'data\themes\pizzatheme'
    if (Test-Path $legacyThemeDest) {
        Remove-Item -Recurse -Force $legacyThemeDest
        Write-Host "[OK] Carpeta antigua en data\themes\pizzatheme eliminada." -ForegroundColor Green
    }

    Write-Host "-> Instalando Pizza Theme (Mod format)..." -ForegroundColor Yellow
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
            Write-Host "[OK] PizzaTheme.mod creado exitosamente en $modDestDir" -ForegroundColor Green
        } else {
            Write-Host "[!] Hubo un error al compilar PizzaTheme.mod." -ForegroundColor Red
        }
    } else {
        Write-Host "[!] No se encontro el script de construccion scripts\build_mod.py" -ForegroundColor Red
    }

    Write-Host "-> Instalando otros Mods..." -ForegroundColor Yellow
    $modSourceDir = Join-Path $scriptPath "mods"
    if (Test-Path $modSourceDir) {
        $sourceMods = Get-ChildItem -Path $modSourceDir -File -Filter "*.mod"
        foreach ($mod in $sourceMods) {
            $prefixLength = [math]::Min(15, $mod.BaseName.Length)
            $prefix = $mod.BaseName.Substring(0, $prefixLength)
            Get-ChildItem -Path $modDestDir -Filter "$prefix*.mod" | Remove-Item -Force -ErrorAction SilentlyContinue
            Copy-Item -LiteralPath $mod.FullName -Destination $modDestDir -Force
        }
        Write-Host "[OK] Todos los mods fueron copiados correctamente." -ForegroundColor Green
    } else {
        Write-Host "[!] No se encontraron mods locales adicionales para copiar." -ForegroundColor DarkYellow
    }
    Write-Host ""
}

Write-Host "[Exito] Todo listo! Ya podes abrir PokeMMO y habilitar el PizzaTheme en Mod Management." -ForegroundColor Green
Write-Host ""
