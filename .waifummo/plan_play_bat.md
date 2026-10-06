## Descripción del Objetivo
Como el estado actual exige comodidad y abstracción, el objetivo es crear un archivo ejecutador (`play.bat`) en la raíz del proyecto. Este archivo abstraerá las "reglas de play" (reglas de ejecución) para que tú, *bebito*, solo tengas que darle doble clic y el sistema se encargue de todo el trabajo pesado por detrás.

Esto aborda la regla #10 de nuestro sistema (`GEMINI.md`), la cual exige activar el entorno virtual y solucionar problemas de codificación de emojis en Windows.

## Propuesta de Cambios

### Scripts de Lanzamiento
Vamos a crear un archivo Batch en la raíz de tu proyecto que sea súper fácil de leer y modificar si el día de mañana cambias los nombres de los archivos.

#### [NEW] `play.bat`
```cmd
@echo off
TITLE Pizzant - The Humanoid Hunter
COLOR 0B

echo ==============================================
echo 🎮 INICIANDO REGLAS DE PLAY (PIZZANT) 🎮
echo ==============================================

:: 1. Forzar codificación UTF-8 para que los emojis del log no rompan la consola
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

:: 2. Activar el entorno virtual (Regla de oro de Python)
echo [1/2] Activando entorno virtual...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No se encontró la carpeta 'venv'. Asegúrate de estar en el directorio correcto.
    pause
    exit /b
)

:: 3. Lanzar la Interfaz Principal
echo [2/2] Levantando la Interfaz Gráfica (main_gui.py)...
python main_gui.py

:: 4. Evitar que la ventana se cierre de golpe si hay un error fatal
pause
```

## User Review Required
> [!IMPORTANT]
> **Aprobación del Launcher**
> ¿Te parece bien el nombre `play.bat` para el archivo? ¿Quieres que agregue algún paso extra antes de levantar el bot (por ejemplo, hacer un `git pull` automático para tener la última versión, o limpiar logs viejos)?

## Plan de Verificación
1. **Prueba Manual:** Generaré el archivo. Te pediré que le des doble clic a `play.bat` desde tu escritorio o explorador de Windows.
2. **Resultado Esperado:** La consola debe abrirse, configurar el UTF-8 en silencio, activar `(venv)` y lanzar tu UI `ShinyHunterGUI` sin crasheos y mostrando los emojis correctamente en la terminal.
