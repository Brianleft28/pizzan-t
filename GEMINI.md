# SØREN - Technical System Prompt & Project Map

Este documento es la **Única Fuente de Verdad**. 

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - **SIEMPRE** recorta la imagen usando las coordenadas de `config.json` antes de analizarla. 

2.  **REACCIÓN INMEDIATA AL TOP HUD (NAME SLOTS)**:
    - El patrullaje **DEBE** detenerse en el milisegundo en que los nombres de los Pokémon sean visibles arriba.
    - No esperar al menú de batalla (botones de abajo) para soltar las teclas.
    - La detección de nombres es la prioridad #1 durante la caminata.

3.  **GUARDIÁN DE INACTIVIDAD (ANTI-STUCK)**:
    - Watchdog de 30s con validación de 9s antes de ejecutar limpieza ('X' + Escape).

4.  **JERARQUÍA DE ESCANEO UNIVERSAL (ANTI-PÉRDIDA)**:
    - Escanear SIEMPRE Horda -> Single en todos los modos.

5.  **LECTURA PERSISTENTE Y ROBUSTA (PP/HP)**:
    - Reintentar hasta 4 veces la lectura. Informar siempre RAW OCR en DEBUG.

6.  **LOG DESCRIPTIVO TOTAL**:
    - Informe detallado de cada turno, oponente y nivel. Ver la patrulla activa en el log.

7.  **ESTRUCTURA MODULAR (v6.5)**:
    - Lógica independiente en `src/modes/`. No añadir lógica de combate en `bot_main.py`.

## 🏗️ Registro de Refactorización (Marzo 2026)
- **Modularización**: Separación de bucles en clases independientes.
- **Interruptible Patrol**: Implementación de caminata que se corta instantáneamente al detectar el Top HUD.
- **PokéLogger**: Gestión centralizada de mensajes con categorías y tiempos.
