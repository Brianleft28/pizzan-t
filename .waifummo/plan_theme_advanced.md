## Plan de Acción: Sincronización de Tema y Fondos (Cero Complacencia)

### [Goal Description] (目的 - Mokuteki)
El usuario notó correctamente que un simple "copiar y pegar" del tema no es suficiente. 
1. La etiqueta `<version>` en el `info.xml` del tema debe coincidir exactamente con la versión actual del juego, de lo contrario PokeMMO no lo carga.
2. Los fondos de batalla (arenas) y *backgrounds* del juego entorpecen la lectura óptica (OCR) del bot. Deben ser reemplazados o eliminados (usualmente a través de *Mods* o archivos gráficos modificados).

**Enfoque de 0 Complacencia:** No usaremos un `.bat` primitivo para modificar XMLs. Usaremos un *script* en Python que parsee el XML nativo del juego, extraiga la versión, y parchee el tema de forma segura, todo envuelto en un `.bat` de 1-click para el usuario.

### Proposed Changes

#### 1. [NEW] `scripts/installer.py`
Un script robusto en Python que se encarga del trabajo pesado:
*   Solicita la ruta de PokéMMO.
*   Lee `[Ruta_PokeMMO]/data/themes/default/info.xml` y extrae la versión oficial actual.
*   Copia la carpeta `assets/pokemmo_theme` hacia `data/themes/PizzantTheme`.
*   Abre `PizzantTheme/info.xml` y actualiza la etiqueta `<version>` para que coincida.
*   *(Opcional)* Copia cualquier archivo de la carpeta `assets/pokemmo_mods/` hacia `data/mods/` para garantizar que la arena de combate y los fondos queden limpios/negros para el OCR.

#### 2. [NEW] `scripts/install_theme.bat`
Un *wrapper* súper sencillo para que el usuario no toque la consola.
```bat
@echo off
echo Iniciando Instalador de Interfaz Pizzant...
call ..\venv\Scripts\activate
python installer.py
pause
```

#### 3. Estructura de Directorios Requerida
Para que esto funcione, en tu local vas a tener que estructurar tus modificaciones estéticas así:
*   `assets/pokemmo_theme/`: Aquí pones tu "plantilla" XML.
*   `assets/pokemmo_mods/` *(opcional)*: Si usas un Mod (archivo `.zip` o carpeta) para quitar el fondo de la batalla ("ditto box sin mundo de fondo"), lo pones aquí para que el script también lo instale automáticamente.

## Open Questions (質問 - Shitsumon)
1. El fondo de batalla que mencionas ("ditto box sin mundo de fondo"), ¿lo quitaste modificando una imagen dentro de la carpeta del **Theme**, o lo hiciste instalando un **Mod** en la carpeta `data/mods`?

## Verification Plan
1. Crear el `installer.py` y el `.bat`.
2. Probar la ejecución: verificar que el `info.xml` copiado tenga la versión actualizada.
