## Plan de Acción: Gestión de la Dependencia del Tema

### [Goal Description] (目的 - Mokuteki)
Evaluar y definir cómo manejar la dependencia estricta del bot hacia tu tema/plantilla de PokéMMO. Actualmente, si otro usuario corre el bot con un tema distinto, las coordenadas de `config.json` no coincidirán y el bot fallará.

Queremos definir si construimos un **Script de Auto-Instalación** o si lo mantenemos como un **Requisito Previo (Manual)**.

---

### Análisis de Soluciones

#### Opción 1: Auto-Instalador (*Deployment Script*)
Empaquetamos tu tema dentro del repositorio del bot y creamos un *script* que lo instala automáticamente en la PC de quien vaya a usarlo.

*   **¿Cómo funciona?**
    1. Guardas tu tema en `assets/pokemmo_theme/`.
    2. Creamos `install_theme.bat`.
    3. El usuario corre el *.bat*, el script busca dónde está instalado PokéMMO y copia la carpeta del tema dentro de `PokeMMO/data/themes/`.
*   **Pros:** Experiencia "1-click" para el usuario. Cero fricción manual.
*   **Contras:** El tema *debe* subirse a GitHub junto con el código fuente del bot.

#### Opción 2: Requisito Previo (*Prerequisite*)
No hay script. Se documenta fuertemente en el `README.md` que el bot requiere X tema para funcionar, y el usuario debe buscarlo, descargarlo y pegarlo en su juego.

*   **Pros:** Menos archivos en el repositorio.
*   **Contras:** Proceso manual, propenso a errores humanos (si lo pegan en la carpeta equivocada, el bot explota).

#### Opción 3: Visión Dinámica (*Computer Vision Compleja*) (❌ Descartada)
Hacer que el bot busque ventanas sin importar el tema mediante *Template Matching* dinámico en toda la pantalla.
*   **Por qué se descarta:** Rompe nuestra regla fundamental **"NO MAREAR AL USUARIO (NO INNOVAR DEMASIADO)"**. Requiere refactorizar todo el motor de visión y puede introducir *lag*.

---

### Proposed Changes (Si elegimos la Opción 1)

1. **[NEW] `assets/pokemmo_theme/`**: Directorio donde colocarás tu interfaz.
2. **[NEW] `scripts/install_theme.bat`**: Script en PowerShell/Batch para localizar el juego y transferir los archivos automáticamente.
3. **[MODIFY] `README.md`**: Explicar que el paso 1 antes de usar el bot es correr el instalador del tema.

## Open Questions (質問 - Shitsumon)
1. ¿Quieres que armemos el script instalador (`Opción 1`) para facilitarles la vida a los demás, o prefieres dejarlo como un requisito netamente manual (`Opción 2`)?
2. Si elegimos el script, ¿tienes la carpeta original de tu tema a mano para incluirla en el proyecto?
