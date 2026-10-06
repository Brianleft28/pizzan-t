## Plan de Acción: Evaluación Arquitectónica (Feedback)

### [Goal Description] (目的 - Mokuteki)
Evaluar la viabilidad técnica de las soluciones propuestas para el empaquetado del bot, específicamente respondiendo al descubrimiento de que el "fondo limpio de batalla" es una configuración nativa del juego (posiblemente un `.ini` o `.properties`) y no un Mod externo.

### Análisis y Feedback (0 Complacencia)

#### 1. Sincronización del Tema (XML Versioning)
*   **Tu idea:** Un script que sincronice la versión para que el juego no rechace el tema.
*   **Mi Feedback:** Es una idea brillante de nivel *DevOps*. Distribuir un tema estático siempre termina en fallos cuando el juego se actualiza. Crear un `installer.py` que lea la versión nativa del juego de quien lo instala y sobrescriba tu tema es la **solución definitiva**. Esto se implementará 100%.

#### 2. El "Ditto Box" sin Fondo (In-Game Options)
*   **Tu idea:** Quizás el mismo script `.bat` puede modificar el archivo `.ini` del juego para forzar esta opción gráfica.
*   **Mi Feedback:** ⚠️ **Alerta de Arquitectura**. Modificar archivos de configuración nativos de un usuario (como la resolución, volumen o gráficos en un `.properties`) desde un script externo es una pésima práctica. Podríamos corromper su cliente de PokéMMO o resetearle configuraciones críticas sin querer, porque el juego reescribe esos archivos constantemente.
*   **La Solución Segura:** *Documentación Preventiva*. En lugar de hackear el `.ini`, el `README.md` tendrá un recuadro enorme de **Paso Cero** indicando la ruta exacta dentro del juego (ej: *Ajustes -> Video -> Desactivar Fondos de Combate*). Esto respeta el entorno del usuario y logra el mismo objetivo para el OCR.

### Proposed Changes
Se ajusta la arquitectura final:
1. **[NEW] `scripts/installer.py`**: Se encarga EXCLUSIVAMENTE de clonar tu tema y parchear el archivo `info.xml` con la versión correcta.
2. **[NEW] `README.md` (Sección Setup)**: Se añade como instrucción estricta desmarcar la opción de "Fondos de Batalla" directamente desde el menú visual de PokéMMO.

## Open Questions (質問 - Shitsumon)
1. ¿Estás de acuerdo con establecer este límite técnico (Instalador automatizado para el Tema + Instrucción manual in-game para los fondos)?
2. ¿Sabes de memoria cómo se llama exactamente esa opción en el menú de PokéMMO para escribirla directamente en la documentación?
