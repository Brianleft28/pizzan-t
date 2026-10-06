## Ejecución de Scripts en PowerShell (実行 (じっこう - Jikkou))

El objetivo es resolver el error al intentar ejecutar el *script* `play.bat` desde la terminal.

### Diagnóstico
*PowerShell* tiene una medida de seguridad nativa que impide ejecutar comandos o *scripts* ubicados en el directorio actual (local) a menos que se especifique su ruta exacta. Esto evita la ejecución accidental de archivos maliciosos.

### Proposed Changes
No se requieren cambios en la base de código. La única modificación es a nivel del *input* del usuario (*command syntax*):
```powershell
.\play.bat
```

## Verification Plan
### Manual Verification
1. Escribir `.\play.bat` (incluyendo el punto y la barra) en la consola.
2. Verificar que la terminal cambie su codificación a `UTF-8` (`chcp 65001`).
3. Verificar que se inicie el bot (Pizzant) correctamente.
