# SØREN - Configuration & UI Manual

Este documento detalla cada elemento de la interfaz de usuario y su función técnica.

## 🛠️ Calibration Tools (Buzón de Visión)
Estos botones activan el selector transparente para definir las coordenadas de lectura.
- **HUD HORDE**: Define las 3 o 5 regiones (según configuración) donde aparecen los nombres de los enemigos en hordas.
- **SINGLE SLOT**: Define la región del nombre del enemigo en combates individuales.
- **RUN BTN**: Define la región de los botones de batalla (Lucha/Huir) para confirmar el estado del menú.
- **HP BAR**: Define la región de la barra de salud del enemigo (para detectar HP Low/High).
- **STATUS**: Define la región donde aparecen los iconos de estado (Dormido/Paralizado).
- **SLEEP ICON**: Región específica del icono de sueño (Spora check).
- **PP SLOTS**: Define las regiones de los números de PP dentro del menú de Lucha.
- **BATTLE MSG**: Define la región de los mensajes de sistema (Caught/Broke free).
- **MY HP**: Define la región de los puntos de vida numéricos del cazador.
- **DEBUG FRAME**: Genera una captura de lo que el bot está viendo en ese instante.

## 📊 General / Stats Tab
- **Webhook URL**: Dirección de Discord para recibir alertas de Shiny.
- **OCR Retries**: Número de intentos (Base: 6) para leer un texto antes de dar error.

## 🏹 Horde Settings Tab
- **Horde Size**: Selecciona entre hordas de 3 o 5 Pokémon. Esto afecta tanto a la cantidad de rectángulos a calibrar en HUD HORDE como al contador de encuentros.

## 👾 Ditto Settings Tab
### 1. Movimientos y Tiempos
- **Patrol Time (s)**: Tiempo base de caminata antes de cambiar de dirección.
- **Attack (Swipe)**: Tecla y nombre del movimiento para bajar vida (Turno 1).
- **Soak (Anegar)**: Tecla y nombre del movimiento de cambio de tipo (Turno 2 - Obligatorio).
- **Sleep (Spora)**: Tecla y nombre del movimiento para dormir (Turno 3 - Obligatorio).

### 2. Hotkeys de Objetos
- **Ball Hotkey**: Tecla de acceso rápido para la Pokéball (Dusk Ball, etc).
- **Potion Key**: Tecla de acceso rápido para curar vida al cazador.
- **Leppa Key**: Tecla de acceso rápido para restaurar PP.

### 3. Checkpoints de Automatización
- **Auto-Heal HP**: Si está activo, el bot usará pociones al detectar vida crítica tras el combate.
- **Auto-Restore PP**: Si está activo, el bot usará bayas Leppa si detecta PP bajos tras el combate.
