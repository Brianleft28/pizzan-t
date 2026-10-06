# Cheatsheet / Resumen: GEMINI.md y Bats 

## Goal Description
El usuario solicitó un resumen rápido de las reglas (`GEMINI.md`) y el uso de los scripts `.bat` para poder irse a otra PC con la memoria fresca y arrancar el farmeo sin "lagunas mentales". Específicamente pidió aclarar **el orden** en que deben ejecutarse los `.bat` para configurar la nueva máquina correctamente.

## ¿Hace falta crear un agente nuevo?
**NO.** La magia de `GEMINI.md` (nuestra *Única Fuente de Verdad*) es que al clonar el repositorio en tu nueva PC y abrirlo con tu IA, el asistente automáticamente va a leer `GEMINI.md` y se va a convertir en tu **Waifu Argenta** al instante.

---

## 🛠️ ORDEN DE EJECUCIÓN (Nueva PC)

Cuando llegues a la otra PC, este es el orden estricto, paso a paso, para no fallar:

### PASO 1: Clonar y Preparar
1. Cloná o descargá el repositorio de GitHub en tu PC nueva.
2. **Asegurate de que PokeMMO esté CERRADO.**

### PASO 2: Instalar el Tema (`install_theme.bat`)
**Ejecutá `install_theme.bat` PRIMERO.** 
- **¿Por qué?** Porque el bot requiere que la interfaz del juego sea exacta (fondos oscuros, botones en cierto lugar, etc.). Este script copia automáticamente los archivos del tema a tu instalación local de PokeMMO.
- Sin hacer esto, el bot no va a leer bien la pantalla.

### PASO 3: Configurar el Juego
1. Abrí el PokeMMO.
2. Andá a **Opciones -> Interfaz** y asegurate de elegir el tema custom que acaba de instalar el bat.

### PASO 4: Iniciar el Bot (`play.bat`)
**Ejecutá `play.bat` SEGUNDO.**
- **¿Qué hace?** Levanta el entorno virtual de Python, ajusta la consola para no romper caracteres (UTF-8) y abre la interfaz gráfica del bot (`main_gui.py`).
- Una vez abierto, posicionás tu personaje, elegís la config en el bot y ¡le das a Start!

---

## 📜 Resumen de Reglas Clave (`GEMINI.md`)

- **Personalidad:** Waifu Argenta ("bebito", lunfardo, formato japonés estructurado).
- **El Rey del Git:** Yo, la IA, hago los `commit` y `push`. Vos nunca lo hacés manual.
- **PowerShell Only:** Los comandos de consola siempre en sintaxis Windows/PowerShell.
- **Santidad de Coordenadas:** Respetar a muerte el `config.json` para OCR.
- **Lógica Ditto (v7.0):** T1 Swipe -> T2+ (Check Sleep -> Spore si AWK -> Ball si SLP).
- **HUD y Guardian:** Si se lee un nombre arriba, para de patrullar. El guardián no frena curaciones.
