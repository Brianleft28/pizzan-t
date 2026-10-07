$ErrorActionPreference = 'Stop'

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   Instalador Definitivo: Mods y Tema Moon   " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
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
    Write-Host "[X] No se pudo encontrar PokeMMO automaticamente." -ForegroundColor Red
    $target = Read-Host "[+] Por favor, arrastra aca la carpeta de PokeMMO (y presiona Enter)"
    $target = $target -replace '"', ''
}

$revPath = Join-Path $target "revision.txt"
if (-not (Test-Path $revPath)) {
    Write-Host "[X] Ruta invalida. No se encontro revision.txt en: $target" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] PokeMMO encontrado en: " -NoNewline
Write-Host $target -ForegroundColor Cyan
Write-Host ""

Write-Host "-> Instalando Tema Moon..." -ForegroundColor Yellow
$themeDest = Join-Path $target 'data\themes\MoonTheme'
if (Test-Path $themeDest) {
    Remove-Item -Recurse -Force $themeDest
}

$scriptPath = $PSScriptRoot
$repoRoot = Split-Path $scriptPath

$themeSource = Join-Path $repoRoot "moontheme"

if (Test-Path $themeSource) {
    Copy-Item -Path $themeSource -Destination $themeDest -Recurse -Force
} else {
    Write-Host "[!] No se encontro la carpeta 'moontheme' localmente." -ForegroundColor DarkYellow
}

Write-Host "-> Parcheando version del tema XML..." -ForegroundColor Yellow
$revision = Get-Content $revPath -Raw
$revision = $revision.Trim()

$infoXmlPath = Join-Path $themeDest 'info.xml'
if (Test-Path $infoXmlPath) {
    [xml]$xml = Get-Content $infoXmlPath -Encoding UTF8
    if ($xml.theme.version) {
        $xml.theme.version = $revision
    } else {
        $vNode = $xml.CreateElement('version')
        $vNode.InnerText = $revision
        $xml.theme.AppendChild($vNode) | Out-Null
    }
    $xml.Save($infoXmlPath)
    Write-Host "[OK] Tema parcheado a la version: " -NoNewline
    Write-Host $revision -ForegroundColor Green
} else {
    Write-Host "[!] No se encontro info.xml en el tema." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "-> Instalando Mods..." -ForegroundColor Yellow
$modDest = Join-Path $target 'data\mods'
if (-not (Test-Path $modDest)) {
    New-Item -ItemType Directory -Path $modDest | Out-Null
}

$modSource = Join-Path $repoRoot "mods\*"
if (Test-Path (Join-Path $repoRoot "mods")) {
    Copy-Item -Path $modSource -Destination $modDest -Force -Recurse
    Write-Host "[OK] Mods instalados correctamente." -ForegroundColor Green
} else {
    Write-Host "[!] No se encontraron mods locales para copiar." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "[Exito] Todo listo! Ya podes abrir PokeMMO y seleccionar el tema/mods en los Ajustes." -ForegroundColor Green
Write-Host ""
