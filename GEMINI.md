# SØREN - Technical System Prompt & Project Map

Este documento es la **Única Fuente de Verdad**. 

## 🔴 MANDATOS CRÍTICOS (Prohibido Revertir)

1.  **SANTIDAD DE LAS COORDENADAS**: 
    - **SIEMPRE** recorta la imagen usando las coordenadas de `config.json` antes de analizarla. 

2.  **LECTURA PERSISTENTE Y ROBUSTA (PP/HP)**:
    - Si una lectura de PP o Vida devuelve un valor inválido (99, ?? o vacio), el bot **DEBE** reintentar la captura y lectura hasta **4 veces** antes de continuar.
    - Esto previene errores por parpadeos de la UI o animaciones de texto.

3.  **TRANSPARENCIA DE DEBUG (RAW OCR)**:
    - En cada lectura de PP o Vida, el bot debe informar el **Texto Crudo (Raw)** leído por el OCR en la categoría DEBUG (ej: `[🔍] RAW OCR: '14/4O'`).

4.  **LOG DESCRIPTIVO TOTAL**:
    - Informe de cada turno: `[Enemy: LOW/HIGH HP]` | `[Hunter: OK/CRITICAL]`.
    - Reporte detallado de PP antes de navegar a un movimiento.

5.  **ESTRUCTURA MODULAR (v6.5)**:
    - Lógica independiente en `src/modes/`. No añadir lógica de combate en `bot_main.py`.

6.  **MÉTRICAS DE SESIÓN**:
    - Contador de sesión que se resetea al presionar START.
    - Reporte ASCII tras cada captura con Tiempo de Sesión y Dittos atrapados.

## 🏗️ Registro de Refactorización (Marzo 2026)
- **Modularización**: Separación de bucles en clases heredadas de `HuntingMode`.
- **PokéLogger**: Clase independiente para gestión de mensajes y marcas de tiempo.
- **Robustness**: Implementación de reintentos múltiples para OCR crítico.
