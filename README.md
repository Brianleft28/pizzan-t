# SØREN - The Humanoid Shiny Hunter

**SØREN** es un asistente de automatización quirúrgica diseñado para PokéMMO, enfocado en la detección de Shinies y la captura optimizada de Dittos. Utiliza visión artificial no invasiva (OCR y análisis de píxeles) para operar de manera indetectable y eficiente.

## 🚀 Características Principales

- **Arquitectura Modular (v6.8)**: Lógica separada por modos (Hordas, Ditto, Single) para máxima estabilidad.
- **Escaneo Universal Anti-Pérdida**: Sin importar el modo, el bot escanea todo el campo de batalla para asegurar que ningún Shiny sea ignorado.
- **Caminata Humanoide**: Patrones de patrullaje con stamina variable, micro-pausas y respuesta instantánea al Top HUD.
- **Sistema Guardián (Anti-Stuck)**: Vigilancia activa de 30 segundos con protocolos de recuperación automática.
- **Captura Inteligente de Ditto**: Gestión estricta de turnos (Swipe, Sleep) con monitoreo dinámico de estado.
- **Transparencia Total**: Logger estilizado en ASCII con reportes de PP, Vida y marcas de tiempo milimétricas.
- **Notificaciones**: Integración nativa con Discord vía Webhooks para alertas remotas.

## 🛠️ Requisitos e Instalación

1. Tener Python 3.10+ instalado.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el panel de control:
   ```bash
   python main_gui.py
   ```

## 📜 Manual de Operación
Consulta el manual detallado de la interfaz y botones en [docs/config.md](docs/config.md). 

## ⚖️ Mandatos de Desarrollo
Las reglas críticas de comportamiento y seguridad están grabadas en [GEMINI.md](GEMINI.md).
