# Walkthrough: Migración a PyQt6 (MVC), Blindaje del OCR y Reparación de Bugs

Esta bitácora documenta la remodelación de la interfaz gráfica, el blindaje de calibración OCR, la reparación del calibrador en segundo plano y la modernización del instalador orquestado.

## 📌 Contexto
1. La interfaz monolítica de 1000 líneas en `CustomTkinter` fue migrada a **PyQt6 (MVC)** en hilos desacoplados.
2. Al guardar la configuración se perdían las zonas de calibración en `config.json`.
3. El calibrador de pantalla (`selector.py`) dependía del mainloop del antiguo CustomTkinter, fallando con errores de hilo en PyQt6.
4. Las métricas de sesión (`session_encounters`) no se acumulaban en los modos Horda y Single, dejando el cálculo de ratio en 0.
5. El instalador orquestado (`manage.py`) carecía de un flujo guiado "Todo en Uno", no sincronizaba la ruta del juego con el Patcher de UI y fallaba en ZIPs con `info.xml` en la raíz.

## 🔨 Cambios Realizados

1. **Reparación del Calibrador (`selector.py`):**
   - Transición de `tk.Toplevel` a una instancia autónoma de `tk.Tk()`.
   - Incorporación de `self.close()` que ejecuta `root.quit()` y `root.destroy()` limpiamente.
   - Ejecución mediante `root.mainloop()` para garantizar que los eventos de dibujo y teclas respondan con fluidez.

2. **Métricas de Sesión y Logs Estructurados (`src/modes/`):**
   - `src/modes/horda.py` y `src/modes/single.py`: Se incrementa `session_encounters` en cada ciclo de escape/batalla.
   - `src/modes/base.py`: Se delega `log()` directamente a `self.bot.log(message, category)` para preservar los colores (`BATTLE`, `PHASE`, `SUCCESS`) en la interfaz gráfica.

3. **Orquestador e Instalador Unificado (`manage.py`, `pizza.bat`, `scripts/core/`):**
   - **Opción 0 en `manage.py`:** Se añadió `0. Instalación Completa Guiada (Todo en Uno)` para ejecutar de forma secuencial la extracción de ROMs, instalación de temas, sincronización XML y aplicación de parches de UI. Se corrigió para reutilizar la instancia de `client` en cada paso sin re-preguntar la ruta.
   - **Blindaje de `xml_sync.py`:** Se arregló la expresión regular que convertía erróneamente `<?xml version="1.0"?>` en `<?xml version="8"?>`, lo que causaba un `SAXParseException` en PokeMMO y hacía desaparecer el mod de la lista. Además, ahora valida la sintaxis con `xml.etree.ElementTree` antes de guardar y repara automáticamente cabeceras dañadas.
   - **Identidad de Mod `PizzaTheme`:** Se ajustó `name="Pizza Theme"` en el `info.xml` del mod para que en el Administrador de Mods de PokeMMO se identifique claramente (y no como `Moonlyze99`).
   - **Forzado de Tema:** Se aseguró que `client.ui.theme=PizzaTheme` quede persistido en `main.properties`.
   - **Sincronización Patcher:** `manage.py` actualiza dinámicamente `patcher_config.json` con la ruta de instalación detectada de PokeMMO.
   - **Extracción de Temas:** `extractor.py` ahora soporta temas empaquetados con `info.xml` tanto en subdirectorios como directamente en la raíz del archivo ZIP.
   - **Estandarización de Identidad:** `pizza.bat` y `play.bat` actualizados a **PizzaHunter**.
   - **Léxico Profesional:** Eliminado el término streamer de los mensajes de consola.

4. **Acceso desde la Interfaz Gráfica (`src/ui/`):**
   - El botón en `tab_general.py` se renombró a `📦 ABRIR INSTALADOR (CLI)`.
   - Al presionarlo en `main_window.py`, se abre automáticamente una consola interactiva ejecutando `pizza.bat`.

## 🧪 Validación Realizada
- **Compilación de Sintaxis:** Todos los módulos modificados compilan con `py_compile`.
- **Test de Selector:** Se validó que `TkSelector` abre, procesa eventos y cierra sin excepciones ni bloqueos.
- **Test de Sincronización XML:** Se ejecutaron pruebas unitarias sobre casos borde (mods corruptos, temas limpios, XMLs inválidos) confirmando que `sync_xml` no rompe la cabecera estándar XML.
- **Verificación en PokeMMO:** Revisión de `mods.log` de PokeMMO confirmando que el error previo era `XML version "8" is not supported`. Con el XML reparado, el juego reconoce los metadatos.
- **Flujo Git:** Cambios consolidados en `fix/xml-sync-and-orchestrator-client`, mergeados a `develop` y `main`, y sincronizados en GitHub.

## 🚀 Cómo Ejecutar el Bot y el Instalador
```powershell
cd C:\Users\7683\Desktop\workspace\pizza-dittos
.\venv\Scripts\activate

# Para abrir la interfaz gráfica:
python main_gui.py

# Para correr el instalador / orquestador:
.\pizza
```
