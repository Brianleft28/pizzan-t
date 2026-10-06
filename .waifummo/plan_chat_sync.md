# Plan: Sync de Conversación (Cerebro de la IA)

## Goal Description
El usuario solicitó una forma de llevarse literalmente *esta misma conversación* (el historial completo, con artifacts y memoria local) a otra PC. Para lograrlo, vamos a crear dos archivos `.bat` que permitan hacer un backup de la carpeta de la conversación activa (`dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1`) hacia el repositorio de Git, y luego restaurarla en la nueva PC.

## Proposed Changes

### `export_chat.bat`
#### [NEW] `export_chat.bat`
Este archivo copiará la carpeta de datos de la IA al repositorio local, lo agregará a Git, y hará un commit y push automático.

```bat
@echo off
chcp 65001 >nul
echo [1/3] Exportando cerebro de la IA (Chat actual)...
xcopy "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1" ".\.chat_backup\" /E /I /H /Y

echo [2/3] Subiendo a GitHub...
git add .chat_backup
git commit -m "chore: backup de conversacion de la IA"
git push origin main

echo [3/3] ¡Listo! Ya podes ir a la otra PC y ejecutar import_chat.bat
pause
```

### `import_chat.bat`
#### [NEW] `import_chat.bat`
Este archivo se ejecutará en la nueva PC para copiar los archivos del repositorio hacia la carpeta interna de Gemini del usuario.

```bat
@echo off
chcp 65001 >nul
echo [1/2] Restaurando cerebro de la IA en esta PC...
xcopy ".\.chat_backup" "%USERPROFILE%\.gemini\antigravity-cli\brain\dab6a3d4-72ff-45ea-898a-cdc9ce4a7ca1\" /E /I /H /Y

echo [2/2] ¡Completado! Ahora podes abrir la extension y buscar el chat en el historial.
pause
```

## Verification Plan
1. Crear ambos archivos en el directorio raíz.
2. Hacer commit inicial (por ser archivos nuevos).
3. Confirmar con el usuario para que ejecute `export_chat.bat`.
