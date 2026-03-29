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
- **Horde Size**: Selecciona entre hordas de 3 o 5 Pokémon. Esto afecta a la calibración y al contador.
- **Test Alarm**: Reproduce el sonido de alerta para verificar el volumen.
- **Stop Alarm**: Detiene el sonido de prueba.

### 🚨 Configuración de la Alarma Sonora
Para que la alarma funcione en hordas, debes:
1. Ir a la carpeta `assets/` del bot.
2. Colocar un archivo de audio llamado **`shiny_alarm.wav`**.
3. **Importante**: Debe ser formato **.WAV**. Si tienes un MP3, conviértelo a WAV.
4. Usa el botón "TEST ALARM" para verificar que se escucha correctamente.

## 👾 Ditto Settings Tab (Configuración Universal de Captura)
*Nota: Estas teclas se usan tanto para Dittos como para Shinies en modo Single.*
### 1. Movimientos y Tiempos
- **Patrol Time (s)**: Tiempo base de caminata antes de cambiar de dirección.
- **Attack (Swipe)**: Tecla y nombre del movimiento para bajar vida (Turno 1).
- **Sleep (Spora)**: Tecla y nombre del movimiento para dormir.

### 2. Hotkeys de Objetos
- **Ball Hotkey**: Tecla de acceso rápido para la Pokéball.
- **Potion Key**: Tecla de acceso rápido para curar vida (Opcional).
- **Leppa Key**: Tecla de acceso rápido para restaurar PP (Automático si PP=0).

### 3. Checkpoints de Automatización
- **Auto-Restore PP**: Si está activo, el bot usará bayas Leppa cuando un movimiento llegue a 0 PP.
