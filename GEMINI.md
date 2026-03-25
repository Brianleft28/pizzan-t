# SØREN - Technical System Prompt & Project Map

Este documento es la **Única Fuente de Verdad**. 

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - **SIEMPRE** recorta la imagen usando las coordenadas de `config.json` antes de analizarla. 

2.  **LOG DESCRIPTIVO TOTAL (OBLIGATORIO)**:
    - **NUNCA** loguear solo "Battle Detected". 
    - **SIEMPRE** incluir el Nombre y Nivel de cada Pokémon detectado (ej: `[⚔️] Detected: Whismur Nv. 45`).
    - En Hordas, listar los 5 Pokémon detectados antes de decidir el escape.

3.  **OBSERVADOR DE HP POR TURNO**:
    - La vida del enemigo y del cazador debe verificarse al **inicio de cada turno**.
    - No usar porcentajes si no son exactos. Usar estados claros: `[Enemy: LOW HP]` o `[Enemy: HIGH HP]`.
    - Si el Hunter HP no se puede leer, reportar `[Hunter HP: UNKNOWN]` y activar alerta visual.

4.  **ESTRUCTURA MODULAR (v6.5)**:
    - Lógica independiente en `src/modes/`. `bot_main.py` es solo el orquestador.

5.  **FILOSOFÍA DE CAMINATA HUMANOIDE**:
    - Pulsaciones variables basadas en `walk_stamina` y `jitter` aleatorio.

6.  **CAPTURA DITTO REACTIVA**:
    - Prioridad: `Swipe -> Soak -> Sleep (Status Monitor) -> Balls`.
    - El Soak es **OBLIGATORIO** en el Turno 2. El Sleep es **OBLIGATORIO** en el Turno 3.

## 🏗️ Registro de Refactorización (Marzo 2026)
- **Modularización**: Separación de bucles en clases heredadas de `HuntingMode`.
- **Logger**: Implementación de prefijos ASCII y marcas de tiempo automáticas.
- **HP/PP Segregados**: Curación de vida y restauración de PP son checkpoints independientes.
