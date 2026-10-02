# SØREN - Master Technical System Prompt

Este documento es la **Única Fuente de Verdad**.

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - Nunca analizar fuera de las regiones recortadas según `config.json`.

2.  **VISIBILIDAD DE CURACIÓN (OBLIGATORIO)**:
    - El bot **DEBE** loguear explícitamente cuándo detecta la necesidad de curar y cuándo se añade a la cola (queue).
    - Ejemplo: `[💊] PP for Spore is 0. Adding to restoration queue.`

3.  **COMPORTAMIENTO DEL GUARDIÁN (WATCHDOG)**:
    - El timer de inactividad debe resetearse en cada acción real: detección de nombres, lectura exitosa de PP/HP o pulsación de tecla.
    - El Guardián **NO DEBE** interrumpir secuencias activas de combate o curación.

4.  **MONITOR DE ESTADO CONTINUO (DITTO MODE)**:
    - A partir del Turno 2, verificar `is_asleep` al inicio de cada turno. Prioridad absoluta: Espora.

5.  **REACCIÓN INMEDIATA AL TOP HUD**:
    - Detener patrullaje al ver el nombre de cualquier Pokémon arriba.

6.  **JERARQUÍA DE ESCANEO UNIVERSAL**:
    - Escaneo Horda -> Single Combat obligatorio en todos los modos.

7.  **DITTO MODE STRICT TURN LOGIC (v7.0)**:
    - Turno 1: Swipe | Turno 2+: Bucle de `Check Sleep -> Spore (si AWK) -> Ball (si SLP)`.

8.  **IDIOMA DE RESPUESTA**:
    - El asistente IA DEBE responder SIEMPRE en ESPAÑOL.

## 🏗️ Mapa del Proyecto
- `src/bot_main.py`: Orquestador y Guardián.
- `src/modes/ditto.py`: Lógica de captura y gestión de colas de curación.

9.  **RESPETO A LA UI ORIGINAL**:
    - Al actualizar o migrar temas, no sobrescribir ciegamente los XML de estructura si estos contienen Custom Layouts o elementos visuales propios (como fondos de login u overlays de HUD). Preservar el arte y la experiencia visual del usuario por encima de la estandarización.

10. **ENTORNO POWERSHELL Y UNICODE (EMOJIS)**:
    - Para iniciar el proyecto en Windows PowerShell, siempre usar `.\venv\Scripts\activate` seguido de `python main_gui.py`.
    - Al hacer prints en consola (stdout) que contengan Emojis (muy usados en los logs de este bot con OCR), tener en cuenta que PowerShell puede arrojar `UnicodeEncodeError`. El logger de la terminal debe manejar esta excepción o forzar el encoding a UTF-8.
