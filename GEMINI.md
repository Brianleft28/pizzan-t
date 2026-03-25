# SØREN - Technical System Prompt & Project Map

Este documento es la **Única Fuente de Verdad**. 

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - **SIEMPRE** recorta la imagen usando las coordenadas de `config.json` antes de analizarla. 

2.  **LECTURA OBLIGATORIA DE PP (DITTO MODE)**:
    - Antes de navegar hacia un movimiento, el bot **DEBE** abrir el menú de Fight, leer los PP del slot correspondiente y devolverlos al Logger.
    - El log debe incluir el nombre del movimiento (ej: `[🔍] False Swipe PP: 14/40`).

3.  **MÉTRICAS DE SESIÓN**:
    - Se debe llevar un conteo de "Dittos por Sesión" que se resetee al presionar START.
    - Se debe calcular y mostrar el Tiempo de Sesión acumulado en cada reporte de captura.

4.  **LOG DESCRIPTIVO TOTAL**:
    - Incluir Nombre y Nivel de cada Pokémon detectado.
    - Informe de HP al inicio de cada turno: `[Enemy: LOW/HIGH HP]` | `[Hunter: OK/CRITICAL]`.

5.  **ESTRUCTURA MODULAR (v6.5)**:
    - Lógica independiente en `src/modes/`. No añadir lógica de combate en `bot_main.py`.

6.  **CAPTURA DITTO REACTIVA**:
    - Prioridad: `Swipe -> Soak -> Sleep (Status Monitor) -> Balls`.
    - Monitor de Estado activo desde el primer intento de dormir.

## 🏗️ Registro de Refactorización (Marzo 2026)
- **Modularización**: Separación de bucles en clases heredadas de `HuntingMode`.
- **Logger**: Implementación de prefijos ASCII y marcas de tiempo automáticas.
- **Session Tracking**: Implementación de cronómetro y contador de sesión independiente del histórico.
