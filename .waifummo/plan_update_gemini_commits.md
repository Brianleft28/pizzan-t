# Plan: Añadir Regla de Commits Automáticos a GEMINI.md

## Goal Description
El usuario preguntó si la regla de que la IA debe encargarse de los commits y pushes estaba ya en la documentación. Tras revisar `GEMINI.md`, se confirmó que no está explícitamente documentada.
El objetivo es agregar esta regla como un mandato crítico (Regla 13) para que en cualquier entorno donde se clone el bot, la IA asuma automáticamente la responsabilidad del control de versiones.

## Proposed Changes

### `GEMINI.md`
#### [MODIFY] `GEMINI.md`
Añadir la regla 13 al final del documento:

```markdown
13. **AUTOMATIZACIÓN DE REPOSITORIO (GIT)**:
    - El usuario NO realizará `git commit` ni `git push` manualmente. Es responsabilidad EXCLUSIVA de la asistente IA confirmar los cambios, realizar los commits con mensajes claros y descriptivos, y pushear a la rama correspondiente (generalmente `main`). El usuario solo debe preocuparse por clonar o hacer `git pull` en sus otros entornos.
```

## Verification Plan
1. Modificar `GEMINI.md` inyectando la nueva regla al final.
2. Hacer un commit general que incluya tanto esta actualización como los cambios pendientes de la velocidad de combate.
3. Hacer `git push` al repositorio remoto.
