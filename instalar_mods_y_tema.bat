@echo off
chcp 65001 >nul
echo ==============================================
echo 🌙 Instalador Definitivo: Mods y Tema Moon 🌙
echo ==============================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$ErrorActionPreference = 'Stop';" ^
"$pokeDirs = @('C:\Program Files\PokeMMO', 'C:\PokeMMO', 'D:\PokeMMO', \"$env:USERPROFILE\Desktop\PokeMMO\");" ^
"$target = $null;" ^
"foreach ($dir in $pokeDirs) { if (Test-Path \"$dir\revision.txt\") { $target = $dir; break } };" ^
"if (-not $target) {" ^
"    Write-Host '❌ No se pudo encontrar PokeMMO automáticamente.' -ForegroundColor Red;" ^
"    $target = Read-Host '👉 Por favor, arrastra acá la carpeta de PokeMMO (y presiona Enter)';" ^
"    $target = $target -replace '\"', '';" ^
"};" ^
"if (-not (Test-Path \"$target\revision.txt\")) { Write-Host '❌ Ruta inválida. No se encontró revision.txt.' -ForegroundColor Red; exit 1 };" ^
"Write-Host '✅ PokeMMO encontrado en: ' -NoNewline; Write-Host $target -ForegroundColor Cyan;" ^
"" ^
"Write-Host '📦 Instalando Tema Moon...' -ForegroundColor Yellow;" ^
"$themeDest = Join-Path $target 'data\themes\MoonTheme';" ^
"if (Test-Path $themeDest) { Remove-Item -Recurse -Force $themeDest };" ^
"Copy-Item -Path '.\moontheme' -Destination $themeDest -Recurse -Force;" ^
"" ^
"Write-Host '⚙️ Parcheando versión del tema (XML)...' -ForegroundColor Yellow;" ^
"$revision = Get-Content (Join-Path $target 'revision.txt') -Raw;" ^
"$revision = $revision.Trim();" ^
"$infoXmlPath = Join-Path $themeDest 'info.xml';" ^
"if (Test-Path $infoXmlPath) {" ^
"    [xml]$xml = Get-Content $infoXmlPath;" ^
"    if ($xml.theme.version) { $xml.theme.version = $revision } else { $vNode = $xml.CreateElement('version'); $vNode.InnerText = $revision; $xml.theme.AppendChild($vNode) | Out-Null };" ^
"    $xml.Save($infoXmlPath);" ^
"    Write-Host '✅ Tema parcheado a la versión: ' -NoNewline; Write-Host $revision -ForegroundColor Green;" ^
"} else {" ^
"    Write-Host '⚠️ No se encontró info.xml en el tema.' -ForegroundColor DarkYellow;" ^
"};" ^
"" ^
"Write-Host '📦 Instalando Mods...' -ForegroundColor Yellow;" ^
"$modDest = Join-Path $target 'data\mods';" ^
"if (-not (Test-Path $modDest)) { New-Item -ItemType Directory -Path $modDest | Out-Null };" ^
"if (Test-Path '.\mods\*') {" ^
"    Copy-Item -Path '.\mods\*' -Destination $modDest -Force -Recurse;" ^
"    Write-Host '✅ Mods instalados correctamente.' -ForegroundColor Green;" ^
"} else {" ^
"    Write-Host '⚠️ No se encontraron mods locales para copiar.' -ForegroundColor DarkYellow;" ^
"}" ^
"" ^
"Write-Host '🎉 ¡Todo listo! Ya podés abrir PokeMMO y seleccionar el tema/mods en los Ajustes.' -ForegroundColor Green;"

echo.
pause
