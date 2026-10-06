## Plan de Acción: Gestión Híbrida del Tema (Opción 1 + 2)

### [Goal Description] (目的 - Mokuteki)
Implementar una solución robusta y amigable para el problema de la dependencia estética del bot. Combinaremos la **Opción 1** (un script instalador) y la **Opción 2** (documentación como requisito previo estricto). De esta forma, explicamos *por qué* es obligatorio, pero damos la herramienta para resolverlo con un solo *click*.

### Proposed Changes

#### 1. [NEW] `docs/theme_dependency.md`
Crearemos un documento exclusivo para explicar la dependencia visual.
*   **Contenido:** Explicará que las coordenadas (OCR, HP, Menús) están fijadas a tu plantilla de PokéMMO actual. Si el tema cambia, el bot queda ciego.
*   **Instrucciones Manuales:** Explicará cómo copiar la carpeta de `assets/pokemmo_theme` a `PokeMMO/data/themes` si el script falla.

#### 2. [MODIFY] `README.md`
Agregaremos una sección de **Requisitos Previos (Prerequisites)** muy clara.
*   **Añadir:** "⚠️ **Requisito Obligatorio:** El bot depende de un tema visual específico para PokéMMO. Lee la [Documentación de la Plantilla](docs/theme_dependency.md)."
*   **Añadir:** Instrucciones para ejecutar `scripts/install_theme.bat`.

#### 3. [NEW] `scripts/install_theme.bat`
Un script simple en *Batch* para automatizar el proceso sin marear al usuario.
```bat
@echo off
echo ==============================================
echo 🎨 Instalador de Tema Pizzant para PokeMMO
echo ==============================================
echo.
echo Arrastra la carpeta donde tienes instalado PokeMMO aqui
echo (por ejemplo, C:\PokeMMO) y presiona Enter.
echo.
set /p "POKEMMO_DIR=Ruta de PokeMMO: "

echo Copiando archivos del tema...
xcopy /E /I /Y "..\assets\pokemmo_theme" "%POKEMMO_DIR%\data\themes\PizzantTheme"

echo.
echo ✅ ¡Plantilla instalada exitosamente! 
echo Abre PokeMMO, ve a Ajustes -^> Interfaz -^> Tema y selecciona "PizzantTheme".
pause
```

## Open Questions (質問 - Shitsumon)
1. ¿El nombre temporal `PizzantTheme` te parece bien para la carpeta que se creará en el juego de los demás usuarios, o prefieres otro nombre?
2. Para que esto funcione, vas a necesitar crear la carpeta `assets/pokemmo_theme` y pegar tu plantilla ahí adentro. ¿Estás de acuerdo?

## Verification Plan
1. Ejecutar el `.bat` pasándole una ruta de prueba.
2. Comprobar que los archivos de Markdown se visualizan correctamente.
