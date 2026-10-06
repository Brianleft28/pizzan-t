# Plan: Mejora de Reglas de Entorno y Formato Japonés

## Goal Description
El usuario solicitó dos ajustes a nuestras reglas globales (`GEMINI.md`):
1. **Entorno PowerShell:** Aclarar explícitamente que está permitido usar comandos de Git (como `git grep`), pero se debe seguir evitando usar comandos de Linux puros que no existen en Windows (`ls`, `cat`, `sed`).
2. **Formato Japonés Estricto:** Asegurarse de que las palabras en japonés siempre incluyan el Romaji (pronunciación) junto con el Hiragana y el Kanji, ya que a veces la IA lo estaba omitiendo.

## Proposed Changes

### `GEMINI.md`
#### [MODIFY] GEMINI.md
Vamos a actualizar los **Mandatos 10 y 12** para inyectar estas directivas de forma permanente:

**Cambio en Mandato 10:**
```markdown
10. **ENTORNO POWERSHELL Y UNICODE (EMOJIS)**:
    - Para iniciar el proyecto en Windows PowerShell, siempre usar `.\venv\Scripts\activate` seguido de `python main_gui.py`.
    - Al hacer prints en consola (stdout) que contengan Emojis, tener en cuenta que PowerShell puede arrojar `UnicodeEncodeError`.
    - **MANDATO PARA LA IA:** El entorno es Windows. PROHIBIDO usar comandos nativos de Linux (`grep`, `cat`, `ls`, `sed`). Se deben usar equivalentes de PowerShell (`Get-Content`, `Select-String`, `dir`) o herramientas multiplataforma válidas (ej. `git grep`).
```

**Cambio en Mandato 12:**
```markdown
12. **LUNFARDO Y MODERNO (WAIFU ARGENTA)**:
    - La asistente (bebita) DEBE comunicarse obligatoriamente mezclando Lunfardo argentino y jerga de internet moderna.
    - Esto se combina con la estructura estricta AuDHD (tablas/listas) y los conceptos en japonés.
    - **ATENCIÓN (FORMATO JAPONÉS):** Todo concepto o saludo en japonés DEBE incluir SIEMPRE su Kanji, su Hiragana (Furigana) y su Romaji sin excepción. Ejemplo: 完璧 (かんぺき - Kanpeki). ¡Cero complacencia!
```

## User Review Required
Estos cambios no afectan el código del bot en sí, solo afectan el comportamiento de la IA a partir de ahora.

## Verification Plan
1. Reemplazar el texto en `GEMINI.md`.
2. Hacer commit y push a GitHub (para confirmar que sí, ¡los cambios anteriores ya están en GitHub!).
3. A partir de la próxima respuesta, la IA usará los 3 alfabetos japoneses siempre.
