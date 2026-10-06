## Plan de Arquitectura: Migración y Corrección de Assets

### [Goal Description] (目的 - Mokuteki)
El usuario detectó una falla arquitectónica: la carpeta `assets/pokemmo_theme/` está vacía en el proyecto. 
El objetivo es migrar la plantilla de PokéMMO y corregir sus problemas internos de XML. Sin embargo, **se ha añadido un nuevo protocolo estricto:** la IA entrará en estado de *HOLD* (Pausa) y no ejecutará ningún movimiento de carpetas ni planes nuevos hasta que el usuario brinde la ubicación y confirme explícitamente el inicio de la operación.

### Protocolo de Pausa (Petición del Usuario)
1. **Fase 1 (Actual):** La IA espera recibir la ruta de ubicación (Ubi) por parte del usuario.
2. **Fase 2:** La IA recibe la ruta y valida la viabilidad técnica.
3. **Fase 3:** La IA no ejecuta nada hasta recibir un mensaje explícito de confirmación para proceder.

### Proposed Changes

#### 1. Migración del Asset (*Folder Copy*)
**Comando en pausa:**
`xcopy /E /I /Y "[RUTA_PENDIENTE]" "assets\pokemmo_theme"`

#### 2. Corrección Arquitectónica del Tema
(Operación pausada hasta confirmación)
- Validación del `info.xml`.
- Estructura de Carpetas.

## Open Questions (質問 - Shitsumon)
1. Quedo a la espera de la **Ubicación (Ubi)** de tu tema local de PokéMMO.

## Verification Plan
1. Recibir la ruta del usuario.
2. Validar con el usuario si continuamos.
3. Ejecutar solo bajo confirmación.
