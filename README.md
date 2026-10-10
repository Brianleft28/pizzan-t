<div align="center">
  <h1>🍕 Pizza-Dittos (WaifuMMO) 🤖</h1>
  <p><strong>El bot inteligente, modular y waifu-friendly para PokéMMO</strong></p>

  <!-- Badges -->
  <p>
    <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://github.com/Brianleft28/pizzan-t"><img src="https://img.shields.io/badge/GitHub-Repository-black.svg?logo=github&logoColor=white" alt="GitHub"></a>
    <a href="https://github.com/Brianleft28/pizzan-t/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  </p>
</div>

<hr>

## 🎌 Acerca del Proyecto

**Pizza-Dittos** (también conocido internamente como *WaifuMMO*) es un bot avanzado de automatización para **PokéMMO**. A diferencia de los bots tradicionales, este proyecto utiliza **Computer Vision e Inteligencia Artificial** para "leer" la pantalla, analizar estados de combate, e interactuar dinámicamente simulando el comportamiento humano (Humanización).

Además, cuenta con un ecosistema completo para administrar modificaciones visuales (temas) y extraer ROMs, gestionado a través de un CLI orquestador unificado.

## 🛠️ Tecnologías y Librerías Principales

El proyecto está construido sobre las siguientes tecnologías:

*   **[Python 3.10+](https://docs.python.org/3/)**: Lenguaje base del proyecto.
*   **[CustomTkinter](https://customtkinter.tomschimansky.com/)**: Interfaz gráfica (GUI) moderna, con modo oscuro y barras laterales.
*   **[EasyOCR](https://jaided.ai/easyocr/)**: Motor de reconocimiento óptico de caracteres (IA) que nos permite "leer" el juego.
*   **[MSS](https://python-mss.readthedocs.io/)**: Captura de pantalla en tiempo real ultrarrápida.
*   **[PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)**: Control automatizado de mouse y teclado.
*   **[Questionary](https://questionary.readthedocs.io/) & [Rich](https://rich.readthedocs.io/)**: Librerías para nuestro *CLI Orchestrator* interactivo, dándole colores y menús de selección amigables.

---

## 🔄 Flujo de Trabajo (Workflow)

Para evitar problemas, todo el proyecto está centralizado alrededor del archivo [manage.py](manage.py) (el orquestador).
El ciclo normal es:

1.  **Ejecutar el Orquestador:** (Abrir `pizza.bat`)
2.  **Preparar el Juego:** Extraer tus ROMs modificadas y aplicar el PizzaTheme.
3.  **Parchar / Sincronizar:** (Solo si hace falta arreglar bugs visuales del theme o xmls).
4.  **Arrancar el Bot:** Desde el mismo menú, ejecutás la interfaz del bot (`main_gui.py`).

---

## 🚀 Instalación y Uso

A continuación, los pasos para dejar el bot listo en tu PC. Hacé click en cada sección para expandirla.

<details>
<summary><b>1. Pre-requisitos (Las ROMs Modificadas)</b></summary>

El bot <b>necesita leer texto con fondo negro</b> durante los combates. Por ello, se requieren unas ROMs modificadas que quitan el escenario 3D de fondo.

> **Importante:** Por temas de Copyright, las ROMs no están en GitHub.
> Escribí a **contactobrianleft@gmail.com** para pedir el Drive con los ZIPs modificados.

Una vez que tengas el `.zip`, dejalo en tu Escritorio.

</details>

<details>
<summary><b>2. Instalación del Repositorio</b></summary>

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
├── config.json           # Configuración (autogenerada)
├── requirements.txt      # Dependencias Python
├── README.md             # Esta documentación
├── scripts/              # Herramientas modulares
│   ├── core/             # Lógica base (pokemmo.py, extractor.py, xml_sync.py)
│   ├── patcher/          # Herramienta de UI patching
│   └── ...               # Otros scripts (build release, migrator)
├── src/                  # Código fuente del bot
│   ├── bot_main.py       # Cerebro (Watchdog y Guardián)
│   ├── vision.py         # Captura de pantalla
│   ├── recognizer.py     # Lógica EasyOCR
│   ├── logger.py         # Consola de colores (Rich)
│   └── modes/            # Lógica de estados
│       ├── base.py       # Modo Base
│       ├── ditto.py      # Modo Ditto
│       ├── horda.py      # Modo Horda
│       └── single.py     # Modo Single
├── pizzatheme/           # Assets visuales para PokéMMO
└── ...
```

---

## ⚖️ Aviso Legal

Este proyecto es de uso **personal y educativo**. El uso de bots puede violar los términos de servicio de PokéMMO. El autor no se responsabiliza por las consecuencias (bans) derivadas de su uso.
