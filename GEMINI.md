# SØREN - Master Technical System Prompt

Este documento es la **Única Fuente de Verdad**.

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - Nunca analizar fuera de las regiones recortadas según `config.json`.

2.  **MONITOR DE ESTADO CONTINUO (DITTO MODE)**:
    - A partir del **Turno 2**, el bot **DEBE** verificar el estado del objetivo (`is_asleep`) al inicio de cada turno.
    - Si el objetivo no está dormido, la prioridad absoluta es usar **Espora**.
    - El bot debe informar en el logger cuando se activa este monitoreo por primera vez.

3.  **REACCIÓN INMEDIATA AL TOP HUD**:
    - Detener patrullaje al ver el nombre de cualquier Pokémon arriba.

4.  **JERARQUÍA DE ESCANEO UNIVERSAL**:
    - Escaneo Horda -> Single Combat obligatorio en todos los modos.

5.  **DITTO MODE STRICT TURN LOGIC (v7.0)**:
    - Turno 1: Swipe (Falso Tortazo).
    - Turno 2+: Bucle de `Check Sleep -> Spore (si AWK) -> Ball (si SLP)`.
    - El movimiento "Soak" ha sido eliminado por completo de la lógica y la UI.

6.  **LECTURA PERSISTENTE DE PP/HP**:
    - 4 reintentos con RAW OCR en DEBUG para valores críticos.

## 🏗️ Mapa del Proyecto
- `src/bot_main.py`: Orquestador de Visión.
- `src/modes/ditto.py`: Lógica reactiva de captura y Monitor de Estado.
- `docs/config.md`: Manual de botones (Actualizado).
