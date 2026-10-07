<# :
@echo off
setlocal
chcp 65001 >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-Command -ScriptBlock ([scriptblock]::Create((Get-Content -Path '%~f0' -Raw)))"
pause
exit /b
#>
$ErrorActionPreference = 'Stop'

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "🌙 Instalador Definitivo: Mods y Tema Moon 🌙" -ForegroundColor Cyan
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
    Write-Host "❌ No se pudo encontrar PokeMMO automáticamente." -ForegroundColor Red
    $target = Read-Host "👉 Por favor, arrastra acá la carpeta de PokeMMO (y presiona Enter)"
    $target = $target -replace '"', ''
}

$revPath = Join-Path $target "revision.txt"
if (-not (Test-Path $revPath)) {
    Write-Host "❌ Ruta inválida. No se encontró revision.txt en: $target" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PokeMMO encontrado en: " -NoNewline
Write-Host $target -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Instalando Tema Moon..." -ForegroundColor Yellow
$themeDest = Join-Path $target 'data\themes\MoonTheme'
if (Test-Path $themeDest) {
    Remove-Item -Recurse -Force $themeDest
}

$scriptPath = $MyInvocation.MyCommand.Path
if (-not $scriptPath) {
    $scriptPath = $env:PWD
} else {
    $scriptPath = Split-Path $scriptPath
}

$themeSource = Join-Path $scriptPath "moontheme"
if (Test-Path $themeSource) {
    Copy-Item -Path $themeSource -Destination $themeDest -Recurse -Force
} else {
    Write-Host "⚠️ No se encontró la carpeta 'moontheme' localmente." -ForegroundColor DarkYellow
}

Write-Host "⚙️ Parcheando versión del tema (XML)..." -ForegroundColor Yellow
$revision = Get-Content $revPath -Raw
$revision = $revision.Trim()

$infoXmlPath = Join-Path $themeDest 'info.xml'
if (Test-Path $infoXmlPath) {
    [xml]$xml = Get-Content $infoXmlPath
    if ($xml.theme.version) {
        $xml.theme.version = $revision
    } else {
        $vNode = $xml.CreateElement('version')
        $vNode.InnerText = $revision
        $xml.theme.AppendChild($vNode) | Out-Null
    }
    $xml.Save($infoXmlPath)
    Write-Host "✅ Tema parcheado a la versión: " -NoNewline
    Write-Host $revision -ForegroundColor Green
} else {
    Write-Host "⚠️ No se encontró info.xml en el tema." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "📦 Instalando Mods..." -ForegroundColor Yellow
$modDest = Join-Path $target 'data\mods'
if (-not (Test-Path $modDest)) {
    New-Item -ItemType Directory -Path $modDest | Out-Null
}

$modSource = Join-Path $scriptPath "mods\*"
if (Test-Path $modSource) {
    Copy-Item -Path $modSource -Destination $modDest -Force -Recurse
    Write-Host "✅ Mods instalados correctamente." -ForegroundColor Green
} else {
    Write-Host "⚠️ No se encontraron mods locales para copiar." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "🎉 ¡Todo listo! Ya podés abrir PokeMMO y seleccionar el tema/mods en los Ajustes." -ForegroundColor Green
Write-Host ""
