<div align="center">
  <h1>🍕 PizzaHunter 🤖</h1>
  <p><strong>El bot inteligente y modular para PokéMMO</strong><br>
  <em>The smart and modular automation bot for PokéMMO</em></p>

  <!-- Badges -->
  <p>
    <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://customtkinter.tomschimansky.com/"><img src="https://img.shields.io/badge/UI-CustomTkinter-blueviolet.svg" alt="CustomTkinter"></a>
    <a href="https://jaided.ai/easyocr/"><img src="https://img.shields.io/badge/AI-EasyOCR-orange.svg" alt="EasyOCR"></a>
    <a href="https://python-mss.readthedocs.io/"><img src="https://img.shields.io/badge/Vision-MSS-yellow.svg" alt="MSS"></a>
    <a href="https://pyautogui.readthedocs.io/"><img src="https://img.shields.io/badge/Control-PyAutoGUI-red.svg" alt="PyAutoGUI"></a>
    <a href="https://github.com/Brianleft28/pizzan-t"><img src="https://img.shields.io/badge/GitHub-Repository-black.svg?logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://github.com/Brianleft28/pizzan-t/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  </p>

  <p>
    <a href="#-español"><b>[🇪🇸 Español]</b></a> &nbsp; | &nbsp; <a href="#-english"><b>[🇬🇧 English]</b></a>
  </p>
</div>

<hr>

# 🇪🇸 Español

## 📑 Índice de Contenidos
1. [Acerca del Proyecto](#-acerca-del-proyecto)
2. [Documentación Técnica y Arquitectura](#-documentación-técnica-y-arquitectura)
3. [Instalación y Uso (Paso a Paso)](#-instalación-y-uso-paso-a-paso)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Aviso Legal](#-aviso-legal)

---

## 🎌 Acerca del Proyecto

**PizzaHunter** es un bot avanzado de automatización para **PokéMMO**. A diferencia de los bots tradicionales que dependen de leer la memoria (RAM) o inyectar código (lo cual conlleva bans inmediatos), este proyecto utiliza **Computer Vision e Inteligencia Artificial** para "leer" la pantalla de forma pasiva, analizar estados de combate, e interactuar dinámicamente simulando el comportamiento humano (Humanización).

Además, cuenta con un ecosistema completo para administrar modificaciones visuales (temas) y extraer ROMs, gestionado a través de un CLI orquestador unificado.

---

## 📚 Documentación Técnica y Arquitectura

<details>
<summary><b>Haz click aquí para desplegar la mega-documentación técnica (Deep Dive)</b></summary>
<br>

Esta sección está destinada a desarrolladores o usuarios curiosos que quieran entender exactamente cómo funciona el bot por debajo del capó.

### 1. El Cerebro (El Bucle Principal)
El archivo **[`src/bot_main.py`](src/bot_main.py)** es el verdadero corazón del bot. Funciona mediante una **Máquina de Estados Finita (Finite State Machine)** dentro de un bucle `while True` (infinito).
*   **Fase 1: Escaneo (Vision & OCR):** Usando **[`src/vision.py`](src/vision.py)** (MSS), el bot toma una captura de pantalla ultrarrápida. Luego, **[`src/recognizer.py`](src/recognizer.py)** (EasyOCR) lee el texto en coordenadas específicas (definidas en `config.json`).
*   **Fase 2: Decisión (Guard dog):** Si el OCR lee "Horde", el bot cambia al estado `ModeHorde`. Si lee "Ditto", cambia a `ModeDitto`.
*   **Fase 3: Acción (Controller):** El archivo **[`src/controller.py`](src/controller.py)** (PyAutoGUI) recibe la orden y ejecuta los clicks o pulsaciones de teclado con un delay aleatorio para evitar sistemas anti-bot (Humanización).

### 2. OCR y Calibración
El bot **está ciego** si no le dices dónde mirar. Para leer texto a gran velocidad sin colapsar tu CPU, el bot solo analiza pequeños rectángulos de tu pantalla (coordenadas `x, y, width, height`).
*   **El problema del fondo:** EasyOCR no puede leer bien texto si el fondo es una ruta, hierba o un bosque 3D.
*   **La solución (ROMs Modificadas):** Requerimos una ROM específica de Pokémon Black/White que altera los archivos del juego para que el fondo de combate sea **100% NEGRO**. Así, el texto blanco resalta perfectamente y la precisión de la IA sube al 99.9%.

### 3. Orquestador CLI (`manage.py`)
Para evitar que el usuario se pierda instalando ROMs o copiando carpetas, construimos un orquestador en consola interactivo usando **Questionary** y **Rich**.
*   **Extractor Mágico:** **[`scripts/core/extractor.py`](scripts/core/extractor.py)** extrae los `.zip` de ROMs de tu escritorio y las envía automáticamente a la carpeta de PokéMMO sin que tengas que tocar nada.

### 4. Flujo de Captura de un Ditto
1.  **Turno 1:** El bot lee "Ditto". Envía la orden de hacer "Falso Tortazo" (`False Swipe`).
2.  **Turno 2+ (Loop):** El bot lee el ícono de estado (Status).
    *   Si el Ditto está despierto (`AWK`), tira "Espora" (`Spore`).
    *   Si el Ditto está dormido (`SLP`), lanza una Pokebola.
3.  **Healing (Curación):** Si Espora se queda sin PPs, el bot pausa la batalla, abre la mochila, y usa una Baya Zanama (Leppa Berry) para restaurar los PPs.

</details>

---

## 🚀 Instalación y Uso (Paso a Paso)

<details>
<summary><b>1. Pre-requisitos (Las ROMs Modificadas)</b></summary>
<br>

El bot <b>necesita leer texto con fondo negro</b> durante los combates. Por ello, se requieren unas ROMs modificadas que quitan el escenario 3D de fondo.

> **Importante:** Por temas de Copyright, las ROMs no están en GitHub.
> Escribí a **contactobrianleft@gmail.com** para pedir el Drive con los ZIPs modificados.

Una vez que tengas el `.zip`, dejalo en tu Escritorio.

</details>

<details>
<summary><b>2. Instalación del Repositorio</b></summary>
<br>

Cloná el repo y prepará el entorno de Python:

```powershell
git clone https://github.com/Brianleft28/pizzan-t
cd pizzan-t

# Crear entorno virtual (obligatorio)
python -m venv venv

# Activar el entorno (hacer esto cada vez que abras la consola)
.\venv\Scripts\activate

# Instalar las librerías (tardará un poco por EasyOCR/PyTorch)
pip install -r requirements.txt
```

</details>

<details>
<summary><b>3. Uso del Orquestador (pizza.bat)</b></summary>
<br>

El proyecto incluye un script facilitador. Simplemente hacé doble click en **[`pizza.bat`](pizza.bat)**.

Aparecerá un menú interactivo (**[`manage.py`](manage.py)**) con opciones numeradas:

1.  **Extraer ZIP de ROMs:** Selecciona esta opción y el script buscará el `.zip` en tu escritorio para instalarlo en el PokéMMO automáticamente. *(Usa [`scripts/core/extractor.py`](scripts/core/extractor.py))*
2.  **Instalar PizzaTheme:** Aplica el tema visual con los fondos negros que necesita el bot.
3.  **Modificar medidas de UI (Patcher):** Parcheador de layouts para monitores específicos. *(Usa [`scripts/patcher/main.py`](scripts/patcher/main.py))*
4.  **Arrancar el Bot:** Abre la interfaz gráfica del bot. *(Abre [`main_gui.py`](main_gui.py))*
5.  **Sincronizar XMLs:** Mantiene la compatibilidad con actualizaciones del juego. *(Usa [`scripts/core/xml_sync.py`](scripts/core/xml_sync.py))*

Sigue el orden del 1 al 4 para tener la experiencia completa.

</details>

<details>
<summary><b>4. Ingame Setup (Dentro de PokéMMO)</b></summary>
<br>

*   Andá a **Ajustes -> Interfaz -> Tema** y seleccioná `PizzaTheme`.
*   En **Ajustes -> Video**, desactivá los fondos de combate.
*   Tu PokéMMO tiene que estar visible en pantalla (no minimizado ni cubierto por otras ventanas).

</details>

---

## 📂 Estructura del Proyecto

```text
pizzan-t/
├── pizza.bat             # Acceso directo rápido
├── manage.py             # Orquestador CLI principal
├── main_gui.py           # GUI y punto de entrada del bot
├── scripts/              # Herramientas modulares (extractor, xml_sync)
├── src/                  # Código fuente del bot
│   ├── bot_main.py       # Cerebro (Watchdog y Guardián)
│   ├── vision.py         # Captura de pantalla
│   ├── recognizer.py     # Lógica EasyOCR
│   ├── logger.py         # Consola de colores (Rich)
│   └── modes/            # Lógica de estados (base, ditto, horda)
└── ...
```

---

## ⚖️ Aviso Legal

Este proyecto es de uso **personal y educativo**. El uso de bots puede violar los términos de servicio de PokéMMO. El autor no se responsabiliza por las consecuencias (bans) derivadas de su uso.

<br><br><hr><br><br>

# 🇬🇧 English

## 📑 Table of Contents
1. [About the Project](#-about-the-project)
2. [Technical Documentation & Architecture](#-technical-documentation--architecture)
3. [Installation & Usage (Step by Step)](#-installation--usage-step-by-step)
4. [Project Structure](#-project-structure)
5. [Disclaimer](#-disclaimer)

---

## 🎌 About the Project

**PizzaHunter** is an advanced automation bot for **PokéMMO**. Unlike traditional bots that rely on reading RAM or injecting code (which leads to instant bans), this project uses **Computer Vision and Artificial Intelligence** to passively "read" the screen, analyze combat states, and interact dynamically to simulate human behavior (Humanization).

---

## 📚 Technical Documentation & Architecture

<details>
<summary><b>Click here to expand the mega-technical documentation</b></summary>
<br>

This section is for developers or curious users who want to understand exactly how the bot works under the hood.

### 1. The Brain (Main Loop)
**[`src/bot_main.py`](src/bot_main.py)** is the heart of the bot. It runs a **Finite State Machine** inside a `while True` loop.
*   **Phase 1: Scanning:** Using **[`src/vision.py`](src/vision.py)** (MSS), it takes an ultra-fast screenshot. Then, **[`src/recognizer.py`](src/recognizer.py)** (EasyOCR) reads the text.
*   **Phase 2: Decision:** If the OCR reads "Horde", it switches to `ModeHorde`. If it reads "Ditto", it switches to `ModeDitto`.
*   **Phase 3: Action:** **[`src/controller.py`](src/controller.py)** (PyAutoGUI) executes clicks or keystrokes with random delays.

### 2. OCR and Calibration
The bot **is blind** if you don't tell it where to look. To read text fast without destroying your CPU, it only crops tiny rectangles from your screen.
*   **The Background Problem:** EasyOCR cannot read text if the background is a 3D forest.
*   **The Solution (Modded ROMs):** We use a modified Pokémon Black/White ROM that forces the combat background to be **100% BLACK**. This boosts AI accuracy to 99.9%.

### 3. CLI Orchestrator (`manage.py`)
To prevent users from getting lost installing ROMs, we built an interactive console orchestrator.
*   **Magic Extractor:** **[`scripts/core/extractor.py`](scripts/core/extractor.py)** extracts the `.zip` from your desktop directly to PokéMMO.

### 4. Ditto Catch Flow
1.  **Turn 1:** Bot reads "Ditto" and uses `False Swipe`.
2.  **Turn 2+:** Bot reads the Status icon. If awake (`AWK`), uses `Spore`. If asleep (`SLP`), throws a Pokeball.
3.  **Healing:** If Spore runs out of PPs, the bot uses a Leppa Berry.

</details>

---

## 🚀 Installation & Usage (Step by Step)

<details>
<summary><b>1. Pre-requisites (Modded ROMs)</b></summary>
<br>

The bot <b>must read text with a black background</b>. You need modded ROMs that remove the 3D backgrounds.

> **Important:** For Copyright reasons, ROMs are not on GitHub.
> E-mail **contactobrianleft@gmail.com** to request the Google Drive link with the modded ZIPs.

Once you have the `.zip`, leave it on your Desktop.

</details>

<details>
<summary><b>2. Repository Installation</b></summary>
<br>

Clone the repo and prepare the Python environment:

```powershell
git clone https://github.com/Brianleft28/pizzan-t
cd pizzan-t
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

</details>

<details>
<summary><b>3. Orchestrator Usage (pizza.bat)</b></summary>
<br>

Double click on **[`pizza.bat`](pizza.bat)**. An interactive menu (**[`manage.py`](manage.py)**) will appear:

1.  **Extract ROMs ZIP:** Automatically installs the modded ROMs.
2.  **Install PizzaTheme:** Applies the visual theme with black backgrounds.
3.  **Patch UI:** Layout patcher for specific monitors.
4.  **Start Bot:** Opens the GUI **[`main_gui.py`](main_gui.py)**.

</details>

<details>
<summary><b>4. Ingame Setup (Inside PokéMMO)</b></summary>
<br>

*   Go to **Settings -> Interface -> Theme** and select `PizzaTheme`.
*   In **Settings -> Video**, disable combat backgrounds.
*   Your PokéMMO must be fully visible on the screen.

</details>

---

## ⚖️ Disclaimer
This project is for **personal and educational** use only. Botting violates PokéMMO's Terms of Service. The author is not responsible for any bans.
