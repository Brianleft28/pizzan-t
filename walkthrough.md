# Walkthrough Arquitectónico: Migración a Questionary para Instalación de ROMs

## 📌 Contexto
El flujo de instalación original utilizaba un script en batch (`instalar_pizza_theme.bat`) y un botón en la interfaz de usuario (`SYNC PIZZA THEME (MOD)`) para inyectar un tema visual. Sin embargo, para mejorar la mantenibilidad y optimizar el proceso (especialmente dado que los fondos de combate del HUD obstaculizaban el OCR), se decidió realizar un cambio estructural masivo.

## 🔨 Cambios Realizados
1. **Interfaz Gráfica (`main_gui.py`)**:
   - Se eliminó el botón `🎨 SYNC PIZZA THEME (MOD)`.
   - Se eliminaron los métodos de compilación y sincronización de hilos (`_sync_theme` y `_run_sync_theme`) que llamaban ciegamente al `.bat`.
   - Se introdujo un botón marcador de posición `📦 INSTALAR ROMS (WIP)` que invoca un nuevo método `_install_roms_wip`, el cual simplemente loguea que esta funcionalidad está en construcción.

## 🚀 Próximos Pasos (Update Planificado)
1. **Transición a Questionary**: El instalador `.bat` será reemplazado por un script de Python interactivo usando `questionary`.
2. **Selección Dinámica**: El nuevo instalador preguntará al usuario y le permitirá seleccionar un archivo ZIP con las ROMs modificadas que se ubicará directamente en el escritorio del sistema (ahorrando tiempo de descompresión y copiado manual).
3. **ROMs Modificadas (Sin HUD)**: La prioridad de esta actualización es asegurar que la ROM modificada (que quita el fondo de batalla) se instale con éxito en el directorio correcto. Esto es imperativo para que el OCR del bot funcione sin ceguera durante los combates de horda y captura de Ditto.

## 📝 Reglas Aplicadas
- **Regla 16**: Documentación de decisiones y cambios arquitectónicos en artefacto Markdown (`walkthrough.md`).
- **Regla 18**: Prevención de problemas en PCs distintas y gestión del OCR que depende vitalmente de la versión *modificada* de la ROM para no tener problemas de lectura.
