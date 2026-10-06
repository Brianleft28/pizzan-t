## Roadmap del Proyecto Pizzant

### [Goal Description] (目的 - Mokuteki)
Este documento sirve como un ancla de memoria para recordar dónde estamos parados, qué problemas ya solucionamos en el código y cuáles son las tareas pendientes que mencionaste.

### Estado Actual (*Current Status*)
1. **Problema de Terminal**: Solucionado. Usamos `.\play.bat` para que los emojis del *logger* no rompan *PowerShell*.
2. **Problema de Captura (Ditto)**: Solucionado. La UI de la Pokédex ahogaba el bot. Implementamos *Active Polling* (`Left -> X`) y extrajimos el `timing_capture_spam_delay` a `0.3` en `config.json`.
3. **Reglas Globales**: Configuradas. El *bot* IA ahora se comunica en formato *Bebita Table*, usa vocabulario técnico en inglés y aplica formato estricto de japonés para el aprendizaje del usuario.

### Tareas Pendientes (*To-Do List*)

#### 1. Cambios Estéticos (*Frontend / UI*)
Mencionaste: *"hay que hacer cambios estéticos y dejar de default la plantilla que tengo ahora"*.
- **Acción Requerida**: Necesito que me confirmes si ya hiciste esos cambios en tus archivos locales, o si necesitas que yo edite algún archivo específico de interfaz gráfica (como `main_gui.py` o algún archivo de temas) para dejarlos como *default*.

#### 2. Control de Versiones (*Git Push*)
Mencionaste: *"luego subirlo a git"*.
- **Acción Requerida**: Una vez asegurados los cambios estéticos (para cumplir con el Mandato 9: *RESPETO A LA UI ORIGINAL* y no pisar tus *custom layouts*), procederemos a hacer el *commit* final y subir todo al repositorio remoto.

## Open Questions
1. ¿Qué archivos de la "plantilla" modificaste o quieres que modifique antes de guardar en *Git*?
2. ¿Testeaste el `0.3` del Ditto in-game y quedó todo funcional?

## Verification Plan
1. Revisar los archivos de UI.
2. Hacer `git status`, `git add`, `git commit` y `git push`.
