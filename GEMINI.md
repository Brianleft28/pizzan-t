# SØREN - Technical System Prompt & Project Map

Este documento es la **Única Fuente de Verdad**. Cualquier agente que trabaje en este código debe seguir estos mandatos o el sistema fallará.

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - **NUNCA** pases un frame completo (`frame`) a las funciones de OCR o Reconocimiento. 
    - **SIEMPRE** recorta la imagen usando las coordenadas de `config.json` antes de analizarla. 
    - Si el usuario calibró una zona, es porque esa es la **única** zona donde está el dato. Leer fuera de ahí provoca falsos positivos (Shinies fantasma).

2.  **BILINGÜISMO OBLIGATORIO**: 
    - Todas las búsquedas de texto deben incluir términos en **Español e Inglés** (ej: "Caught" y "Atrapado"). No asumas el idioma del cliente.

3.  **CERO LECTURA DE CHAT PARA DECISIONES**: 
    - El chat es ruido. Usa el **Nombre del Pokémon** (arriba) para identificar y el **Menú de Batalla** (Huir/Luchar) para confirmar el turno. Solo usa el mensaje de batalla para confirmar el éxito de la Ball.

## 🏗️ Arquitectura de Visión (v2.6 Surgical)

### 1. Identificación Quirúrgica
- El flujo de entrada es: `Detección de Letras en Slot` -> `Recorte Estricto` -> `OCR de Nombre` -> `Esperar Menú`.
- Si el OCR se ejecuta sobre la pantalla completa, el bot detectará palabras como "Shiny" o "Ditto" dentro de su propio Logger o GUI, entrando en bucles infinitos de error.

### 2. Monitor de Vida por Turno
- La vida se lee en cada inicio de turno mediante el recorte de `hunter_hp_region`.
- El bot debe informar: `Target HP %`, `Target Status` y `Hunter HP/Total`.

## ⚙️ Esquema de Configuración (`config.json`)
- `slot_single`: Región del nombre del enemigo.
- `hp_bar_region`: Región de la barra de salud del enemigo.
- `battle_msg_region`: Región de los mensajes de sistema (Caught/Broke free).
- `hunter_hp_region`: Región de la vida numérica del cazador.

## 🛠️ Diagnóstico (Botón Debug)
- El botón **DEBUG FRAME** debe generar `debug_view.png` mostrando la pantalla procesada en blanco y negro (Threshold 160). 
- **Propósito**: Si el usuario ve la imagen blanca o negra, debe ajustar el brillo del juego o el tema (Dark/Light).
