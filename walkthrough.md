# Walkthrough: Migración a PyQt6 (MVC) y Blindaje del OCR

Esta bitácora documenta la remodelación completa de la interfaz gráfica y la corrección crítica del guardado de coordenadas para el motor OCR.

## 📌 Contexto
La interfaz monolítica de 1000 líneas en `CustomTkinter` presentaba bloqueos en el hilo principal durante el reconocimiento EasyOCR y el visor de código. Además, al guardar la configuración desde la interfaz, se sobrescribían ciegamente las coordenadas de calibración de regiones en `config.json`, dejando el bot incapacitado de leer la pantalla de PokeMMO.

## 🔨 Cambios Realizados

1. **Migración a PyQt6 con Arquitectura MVC (`src/ui/`):**
   - **Vistas Modulares (`src/ui/views/`):** Desacople en componentes independientes:
     - `header_bar.py`: Control de inicio/detención y selector de modo.
     - `stats_bar.py`: Métricas en tiempo real.
     - `logger_widget.py`: Consola reactiva con colores e historial.
     - `brain_viewer.py`: Visor de código con `QSyntaxHighlighter` sin lag.
     - `tabs/`: Pestañas organizadas (`tab_general.py`, `tab_horde.py`, `tab_ditto.py`, `tab_calib.py`).
   - **Controlador en Segundo Plano (`src/ui/controllers/bot_controller.py`):**
     - Aislamiento del bot en un `QThread` con señales `pyqtSignal`. Cero bloqueos de ventana.
   - **Punto de Entrada (`main_gui.py`):** Reducido a ~15 líneas limpias. La versión anterior se preservó como `main_gui_legacy.py`.

2. **Blindaje de Regiones OCR (`src/ui/controllers/config_controller.py`):**
   - Se ajustó el método `save()` para realizar un merge con el contenido previo en disco de `config.json`.
   - Se garantiza la persistencia intacta de `slots`, `slot_single`, `button_run`, `hp_bar_region`, `status_slot_region`, `pp_slots`, `battle_msg_region` y `hunter_hp_region`.

3. **Entorno y Dependencias (`requirements.txt`):**
   - Instalación y validación de `PyQt6>=6.5.0` en el entorno virtual (`venv`).

## 🧪 Validación Realizada
- **Test de importaciones:** `PyQt6`, `easyocr`, `mss`, `cv2` validados sin excepciones.
- **Compilación de módulos:** Todos los archivos en `src/ui/` compilan sin errores.
- **Prueba de preservación:** Guardado de `AppConfig` comprobado mediante script de testing sin pérdida de claves de calibración.
- **Inicialización de interfaz:** `MainWindow` se instancia y arranca de manera limpia.

## 🚀 Cómo Ejecutar el Bot
```powershell
cd C:\Users\7683\Desktop\workspace\pizza-dittos
.\venv\Scripts\activate
python main_gui.py
```
O mediante el acceso rápido: `.\pizza` -> Opción 4 (`Arrancar el Bot`).
