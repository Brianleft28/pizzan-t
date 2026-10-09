# 🇦🇷 SØREN — The Humanoid Shiny Hunter v7.0

**SØREN** es un bot de automatización para **PokéMMO** que detecta Shinies y captura Dittos usando visión artificial no invasiva (OCR + análisis de píxeles). Funciona sin tocar la memoria del juego.

---

## 🎌 Personalidad del Proyecto (Waifu Argenta)
Este proyecto está construido bajo una **filosofía AuDHD estricta (0 complacencia)**. La IA detrás del desarrollo opera bajo un sistema único que mezcla:
- 📊 **Estructuras estrictas** (Tablas y Listas).
- 🎌 **Conceptos en Japonés** (Kanji (Hiragana - Romaji)).
- 🧉 **Lunfardo Argentino y jerga Moderna** (*¡Zarpado, basadísimo y god!*).

---

## ✨ Características v7.0

| Feature | Descripción |
|---|---|
| 🏹 **Modo Horda** | Sweet Scent → escanea 5 slots → pausa y alerta si encuentra Shiny |
| 👾 **Modo Ditto** | Patrulla → detecta Ditto por OCR → Swipe → Spore → Ball |
| 🔮 **Modo Single** | Patrulla → captura cualquier Shiny en combate individual |
| 🌈 **Logger con colores** | Colores reales en la GUI por categoría (BATTLE, HEAL, SUCCESS...) |
| 🧠 **Brain Viewer** | Pestaña en la GUI para leer el código fuente Python en tiempo real |
| 📊 **Stats Bar** | Encounters, Dittos, rate/min y tiempo de sesión siempre visibles |
| ⏱️ **Timings configurables** | OCR wait, settle time, Leppa pre-wait: todo editable desde la UI |
| 💊 **Auto-Heal PP** | Restaura PP con Leppa Berry automáticamente al llegar a 0 |
| 🚨 **Anti-Captcha** | Detección de texto sospechoso + alerta Discord + alarma sonora |
| 🎮 **Humanización** | Caminata con stamina variable, micro-pausas y respuesta al HUD |

---

## 🖥️ Requisitos del Sistema

- **Windows 10/11** (64-bit)
- **Python 3.10 o superior** → [python.org/downloads](https://www.python.org/downloads/)
- **Git** → [git-scm.com](https://git-scm.com/)
- **PokéMMO** corriendo en pantalla (no minimizado)

---

## 🚀 Instalación (PC nueva)

### 1. Clonar el repositorio y Rom Packs

```powershell
git clone https://github.com/Brianleft28/pizzan-t
cd pizzan-t
```

> ⚠️ **Importante (ROMs modificadas):** Recordá copiar tu carpeta de `roms/` (o los archivos de las ROMs modificadas que quitan el fondo de batalla) desde tu PC anterior a la carpeta de tu cliente de PokéMMO en esta nueva PC. Esto es CRÍTICO para que el OCR del bot funcione correctamente al tener un fondo limpio.

### 2. Crear el entorno virtual

```powershell
python -m venv venv
```

### 3. Activar el entorno virtual

> ⚠️ **Importante:** Siempre activar el venv antes de correr el bot. En PowerShell:

```powershell
.\venv\Scripts\activate
```

Vas a ver `(venv)` al inicio de la línea cuando esté activo.

### 4. Instalar dependencias

```powershell
pip install -r requirements.txt
```

> ⏳ La primera vez puede tardar varios minutos porque descarga PyTorch y EasyOCR (~2GB).

### 5. Instalar Tema Visual (Requisito Obligatorio)

El bot usa visión artificial calibrada para una **plantilla específica** y requiere que los fondos de combate estén desactivados. El tema ahora está estructurado de forma moderna como un Mod (.mod).

1. Inicia la interfaz del bot (`python main_gui.py`).
2. Ve a la pestaña **⚙️ General** y presiona el botón **"🎨 SYNC PIZZA THEME (MOD)"**.
3. Espera a que el log interno te confirme que se copió correctamente.
4. Abre PokéMMO, ve a **Administración de Mods** y activa `PizzaTheme`.
5. En **Ajustes -> Video**, **desactiva** la opción de fondos de combate para que el OCR funcione.

### 6. Iniciar el bot

```powershell
python main_gui.py
```

---

## 🔄 Actualizar desde GitHub (cuando hay cambios)

```powershell
git pull origin main
```

No hace falta reinstalar dependencias salvo que haya un cambio en `requirements.txt`.

---

## 🛠️ Calibración (primera vez en una PC)

Antes de usar el bot tenés que calibrar las regiones de la pantalla para que el OCR sepa dónde mirar. En la pestaña **🔧 Calib** de la GUI:

1. **HUD HORDE** → Los nombres de los Pokémon en hordas
2. **SINGLE SLOT** → El nombre del Pokémon en combate individual
3. **RUN BTN** → El botón de "Lucha/Huir" (para saber si estamos en batalla)
4. **HP BAR** → La barra de vida del enemigo
5. **STATUS** → El ícono de estado (dormido, paralizado, etc.)
6. **PP SLOTS** → Los números de PP dentro del menú de Lucha
7. **BATTLE MSG** → El área del mensaje "¡Atrapado!" / "¡Rompió libre!"

Cada botón abre una pantalla de selección: arrastrá para marcar la región y presioná **Enter** para guardar.

---

## ⚙️ Configuración Rápida

### Pestaña 👾 Ditto

| Campo | Qué es |
|---|---|
| Patrol Time | Segundos de caminata antes de cambiar dirección |
| Attack (Clave/Nombre) | Tecla y nombre del movimiento de Turno 1 (ej: `2` / `False Swipe`) |
| Sleep (Clave/Nombre) | Tecla y nombre del movimiento de sueño (ej: `1` / `Spore`) |
| Ball Hotkey | Tecla de acceso rápido de la Pokébola (ej: `5`) |
| Leppa Key | Tecla de la Leppa Berry para restaurar PP (ej: `4`) |

### ⏱️ Timings de Captura (críticos para evitar bugs)

| Campo | Default | Descripción |
|---|---|---|
| OCR Wait | `0.5s` | Espera antes de leer el mensaje de captura (para la animación) |
| Settle | `2.5s` | Espera para cerrar diálogos post-captura |
| Leppa Pre-Wait | `1.5s` | Espera para que cargue el mapa antes de usar Leppa |
| Ball Press Delay | `0.7s` | Delay entre presionar la pokébola y confirmar |

### Pestaña 🏹 Horde

- **Horde Size**: 3 o 5 Pokémon
- **Alarma**: Colocar un archivo `assets/shiny_alarm.wav` para la alerta sonora

---

## 📁 Estructura del Proyecto

```
pizzan-t/
├─ instalar_pizza_theme.bat # Instalador del tema (.mod format)
├─ pizzatheme/          # Archivos crudos del tema visual
├── main_gui.py          # Interfaz gráfica (CustomTkinter)
├── config.json          # Configuración y calibración (auto-generado)
├── selector.py          # Herramienta de calibración de regiones
├── src/
│   ├── bot_main.py      # Orquestador principal y Guardián
│   ├── controller.py    # Input: teclas, movimientos, secuencias
│   ├── vision.py        # Captura de pantalla (mss)
│   ├── recognizer.py    # OCR (EasyOCR) + template matching
│   ├── logger.py        # Logger con colores y buffer circular
│   └── modes/
│       ├── base.py      # Lógica base: captura, patrulla, curación
│       ├── ditto.py     # Modo Ditto
│       ├── horda.py     # Modo Horda
│       └── single.py    # Modo Single
├── docs/
│   └── config.md        # Manual detallado de la UI
└── assets/
    └── shiny_alarm.wav  # Alarma sonora (agregar manualmente)
```

---

## 🐛 Solución de Problemas Comunes

### ❌ `UnicodeEncodeError` al arrancar en PowerShell
El bot usa emojis en los logs. PowerShell puede fallar con caracteres especiales. El logger lo maneja automáticamente, pero si falla la terminal, usá:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### ❌ El bot no detecta la batalla
Recalibrar las regiones **HUD HORDE** y **SINGLE SLOT** en la pestaña 🔧 Calib.

### ❌ Spam de pokébolas / no reconoce la captura
Aumentar el valor de **OCR Wait** en los Timings de Captura (probar `1.0` o `1.5`).

### ❌ La Leppa se usa en el momento equivocado
Aumentar el valor de **Leppa Pre-Wait** (probar `2.0` o `2.5`).

### ❌ `-eenv` o `-env` no reconocidos en PowerShell
Esos no son comandos válidos. El comando correcto para activar el venv es:
```powershell
.\venv\Scripts\activate
```

---

## 📜 Documentación Adicional

- [Manual de la interfaz](docs/config.md) — descripción detallada de cada botón y campo
- [GEMINI.md](GEMINI.md) — mandatos críticos de comportamiento del bot (para desarrolladores)

---

## ⚖️ Aviso Legal

Este proyecto es de uso **personal y educativo**. El uso de bots puede violar los términos de servicio de PokéMMO. El autor no se responsabiliza por consecuencias derivadas de su uso.
