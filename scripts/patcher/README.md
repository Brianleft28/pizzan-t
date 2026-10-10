# PokeMMO UI Patcher

**[English](#english) | [Espanol](#espanol)**

---

<a id="english"></a>

## English

Tool that automatically resizes PokeMMO game windows that are too small by default.

### The problem

Some players manually edit the game's XML files to make windows bigger (inventory, mods panel, shiny encounter tracker). The problem is that **every time the game updates, those changes are lost** and you have to redo them by hand.

### The solution

This patcher does it automatically. You run a `.bat` file and you're done: all the windows you configured get the size you want. If the game updates and resets the changes, just run the patcher again.

### What windows can be modified

| Window                       | What changes           | Original value | Recommended |
| ---------------------------- | ---------------------- | -------------- | ----------- |
| Inventory                    | Min width and height   | 530x378        | 530x567     |
| Mods Panel                   | Min height             | 300            | 1000        |
| Encounter Counter Frame      | Min width / max height | 540 / 340      | 540 / 600   |
| Shiny history scrollpane     | Min height             | 260            | 420         |
| Encounter summary scrollpane | Min height             | 260            | 420         |

### How to use it

#### Option A: Using `configuration.exe` (recommended — no Python required)

1. Open the `pokemmo_ui_patcher` folder
2. Double click **`configuration.exe`**
3. Adjust values, set the game path if needed, then click **Save**
4. Click **"▶ Apply Patches"** directly from the GUI
5. Done. Open the game and the windows will have the new size

To restore original values, click **"↩ Restore Game Defaults"** inside the same GUI.

#### Option B: Using `.bat` files (requires Python 3.10+)

If you prefer the classic method or don't want to use the exe:

1. Install **Python 3.10 or higher**: https://www.python.org/downloads/ (check **"Add Python to PATH"**)
2. **(Optional)** Double click **`open_config.bat`** to open the configuration editor
3. Double click **`run_patcher.bat`**
4. To restore original values: double click **`restore_defaults.bat`**

### How it works

When you run `run_patcher.bat`, this is what happens behind the scenes:

1. It launches `main.py` using Python
2. `main.py` reads your configuration from `patcher_config.json` (game path, themes, patch values)
3. For each enabled theme, it locates the XML files that define the game's UI layout (e.g. `ui/inventory.xml`, `ui/settings.xml`, `main-widgets.xml`)
4. Before modifying any file, it creates an automatic backup in a `.pokemmo_patcher_backups` folder
5. It navigates the XML tree to find the specific `<theme>` and `<param>` nodes, then updates their values (min width, min height, max height, etc.)
6. Shows a summary of all changes in the console

`restore_defaults.bat` does the same process but writes the original game values back instead.

### How to configure values

You have two options:

#### Option 1: Graphical editor (recommended)

Double click **`configuration.exe`** (or **`open_config.bat`** if you prefer using Python). A window will open where you can:

- Set the game installation path (with a folder browser)
- **Automatically detects installed themes** — scans your game's `data/mods/` folder for custom themes that contain a `theme.xml` file, and shows them as checkboxes alongside `default`
- Enable/disable each patch and adjust its values with spinboxes
- **Apply patches or restore defaults directly** with the action buttons
- Reset the form to defaults with one click
- Refresh theme detection after changing the game path

#### Option 2: Edit JSON manually

Open `patcher_config.json` with any text editor and change the numbers:

```json
{
  "game_path": "C:\\Program Files\\PokeMMO",
  "themes": ["default", "´PizzaTheme´"],
  "patches": {
    "inventory": {
      "enabled": true,
      "minWidth": 530,
      "minHeight": 567
    },
    "mods_panel": {
      "enabled": true,
      "minHeight": 1000
    }
  }
}
```

- **game_path**: Path where PokeMMO is installed
- **themes**: List of themes to patch. `"default"` is the base game theme. If you use a custom theme like Moonlyze99, add it to the list
- **patches**: Each window with its values. Set `"enabled": false` to skip a window you don't want to change

### After a game update

If the game updated and the windows went back to their original size, just run `run_patcher.bat` again. Your configured values are kept in `patcher_config.json`.

### Backups

Every time the patcher modifies a file, it first creates an automatic backup in a `.pokemmo_patcher_backups` folder next to the original file. If something goes wrong, the backups are there.

### Project files

```
pokemmo_ui_patcher/
  configuration.exe       <- Double click to open the all-in-one GUI (no Python needed)
  run_patcher.bat         <- Alternative: apply patches from terminal (runs main.py)
  restore_defaults.bat    <- Alternative: restore original values (runs main.py --restore)
  open_config.bat         <- Alternative: open the config editor via Python (runs config_gui.py)
  patcher_config.json     <- Your configuration: game path, themes, and patch values
  config_gui.py           <- Graphical configuration editor source (tkinter)
  main.py                 <- Main script: reads config, applies/restores patches
  config.py               <- Defines which UI windows can be patched and their defaults
  xml_engine.py           <- Finds and modifies <param> nodes inside game XML files
  backup.py               <- Creates timestamped backups before any file is modified
  build_exe.py            <- Builds configuration.exe using PyInstaller
```

---

<a id="espanol"></a>

## Español

Herramienta que agranda automaticamente las ventanas del juego PokeMMO que son demasiado chicas por defecto.

### El problema

Algunos jugadores modifican manualmente los archivos XML del juego para agrandar ventanas como el inventario, el panel de mods o el tracker de encuentros shiny. El problema es que **cada vez que el juego se actualiza, esos cambios se pierden** y hay que volver a hacerlos a mano.

### La solucion

Este patcher lo hace automatico. Ejecutas un archivo `.bat` y listo: todas las ventanas que configuraste quedan con el tamano que quieras. Si el juego se actualiza y se pierden los cambios, solo hay que volver a ejecutar el patcher.

### Que ventanas se pueden modificar

| Ventana                              | Que cambia              | Valor original | Valor recomendado |
| ------------------------------------ | ----------------------- | -------------- | ----------------- |
| Inventario                           | Alto y ancho minimo     | 530x378        | 530x567           |
| Panel de Mods                        | Alto minimo             | 300            | 1000              |
| Frame del Encounter Counter          | Ancho min / alto maximo | 540 / 340      | 540 / 600         |
| Scrollpane del historial shiny       | Alto minimo             | 260            | 420               |
| Scrollpane del resumen de encuentros | Alto minimo             | 260            | 420               |

### Como usarlo

#### Opcion A: Usando `configuration.exe` (recomendado — no necesita Python)

1. Abre la carpeta `pokemmo_ui_patcher`
2. Doble click en **`configuration.exe`**
3. Ajusta los valores, configura la ruta del juego si es necesario, y haz click en **Save**
4. Haz click en **"▶ Apply Patches"** directamente desde la interfaz
5. Listo. Abre el juego y las ventanas tendran el nuevo tamano

Para restaurar los valores originales, haz click en **"↩ Restore Game Defaults"** dentro de la misma interfaz.

#### Opcion B: Usando archivos `.bat` (requiere Python 3.10+)

Si prefieres el metodo clasico o no quieres usar el exe:

1. Instala **Python 3.10 o superior**: https://www.python.org/downloads/ (marca **"Add Python to PATH"**)
2. **(Opcional)** Doble click en **`open_config.bat`** para abrir el editor de configuracion
3. Doble click en **`run_patcher.bat`**
4. Para restaurar valores originales: doble click en **`restore_defaults.bat`**

### Como funciona

Cuando ejecutas `run_patcher.bat`, esto es lo que pasa internamente:

1. Lanza `main.py` usando Python
2. `main.py` lee tu configuracion de `patcher_config.json` (ruta del juego, temas, valores de parches)
3. Para cada tema habilitado, busca los archivos XML que definen la UI del juego (ej: `ui/inventory.xml`, `ui/settings.xml`, `main-widgets.xml`)
4. Antes de modificar cualquier archivo, crea un backup automatico en una carpeta `.pokemmo_patcher_backups`
5. Navega el arbol XML para encontrar los nodos `<theme>` y `<param>` especificos, y actualiza sus valores (ancho minimo, alto minimo, alto maximo, etc.)
6. Muestra un resumen de todos los cambios en la consola

`restore_defaults.bat` hace el mismo proceso pero escribe los valores originales del juego en vez de los configurados.

### Como configurar los valores

Tienes dos opciones:

#### Opcion 1: Editor grafico (recomendado)

Doble click en **`configuration.exe`** (o **`open_config.bat`** si prefieres usar Python). Se abrira una ventana donde puedes:

- Configurar la ruta de instalacion del juego (con un explorador de carpetas)
- **Detecta automaticamente los temas instalados** — escanea la carpeta `data/mods/` del juego buscando temas custom que contengan un archivo `theme.xml`, y los muestra como checkboxes junto a `default`
- Habilitar/deshabilitar cada parche y ajustar sus valores con spinboxes
- **Aplicar parches o restaurar valores originales directamente** con los botones de accion
- Resetear el formulario a los valores por defecto con un click
- Refrescar la deteccion de temas despues de cambiar la ruta del juego

#### Opcion 2: Editar el JSON manualmente

Abre `patcher_config.json` con cualquier editor de texto y cambia los numeros:

```json
{
  "game_path": "C:\\Program Files\\PokeMMO",
  "themes": ["default", "PizzaTheme"],
  "patches": {
    "inventory": {
      "enabled": true,
      "minWidth": 530,
      "minHeight": 567
    },
    "mods_panel": {
      "enabled": true,
      "minHeight": 1000
    }
  }
}
```

- **game_path**: Ruta donde esta instalado PokeMMO
- **themes**: Lista de temas a parchear. `"default"` es el tema base del juego. Si usas un tema custom como Moonlyze99, agregalo a la lista
- **patches**: Cada ventana con sus valores. Pon `"enabled": false` para saltar una ventana que no quieras cambiar

### Despues de una actualizacion del juego

Si el juego se actualizo y las ventanas volvieron a su tamano original, solo vuelve a ejecutar `run_patcher.bat`. Los valores que configuraste se mantienen en `patcher_config.json`.

### Backups

Cada vez que el patcher modifica un archivo, primero crea una copia de seguridad automatica en una carpeta `.pokemmo_patcher_backups` junto al archivo original. Si algo sale mal, los backups estan ahi.

### Archivos del proyecto

```
pokemmo_ui_patcher/
  configuration.exe       <- Doble click para abrir la interfaz todo-en-uno (no necesita Python)
  run_patcher.bat         <- Alternativa: aplicar parches desde terminal (ejecuta main.py)
  restore_defaults.bat    <- Alternativa: restaurar valores originales (ejecuta main.py --restore)
  open_config.bat         <- Alternativa: abrir el editor via Python (ejecuta config_gui.py)
  patcher_config.json     <- Tu configuracion: ruta del juego, temas y valores de parches
  config_gui.py           <- Codigo fuente del editor grafico (tkinter)
  main.py                 <- Script principal: lee config, aplica/restaura parches
  config.py               <- Define que ventanas de la UI se pueden parchear y sus valores por defecto
  xml_engine.py           <- Busca y modifica nodos <param> dentro de los XML del juego
  backup.py               <- Crea backups con timestamp antes de modificar cualquier archivo
  build_exe.py            <- Compila configuration.exe usando PyInstaller
```

---

## Creditos / Credits

Herramienta creada para la comunidad de PokeMMO, basada en el descubrimiento de jugadores que encontraron como modificar los tamanos de ventana editando los XML del juego.

Tool created for the PokeMMO community, based on the discovery by players who found how to modify window sizes by editing the game's XML files.
