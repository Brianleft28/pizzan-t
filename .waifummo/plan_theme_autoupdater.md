## Sincronización Automática de Temas (Auto-Updater) - Plan Definitivo

> [!NOTE] Contexto
> Aplicando nuestra regla global de **NO MAREAR AL USUARIO (NO INNOVAR DEMASIADO)**, hemos descartado cualquier solución compleja (como procesos en segundo plano o *web scraping*). La solución será directa, manejable y reutilizará lo que ya tenemos.

## 🔴 0 Complacencia - Decisión Final de Arquitectura
1. **Punto de Inyección Simple:** Se ejecutará una sola función durante el arranque del bot (`bot_main.py` o `main_gui.py`).
2. **Reutilización de Código:** No crearemos un sistema nuevo. Refactorizaremos tu actual `installer.py` para que exponga una función `auto_sync_theme()` importable.
3. **Fail-Safe Silencioso:** Si falla por alguna razón (ej. PokeMMO cambia la estructura de sus carpetas), capturamos la excepción, la mostramos en el log de PowerShell, y el bot continúa su ejecución sin crashear.

## Proposed Changes

### [MODIFY] `scripts/installer.py`
Refactorización para que no solo sea un *script* ejecutable, sino un módulo limpio.

```python
import os
import xml.etree.ElementTree as ET

def auto_sync_theme(game_dir, theme_dir):
    """
    Sincroniza la versión del info.xml del juego con el custom theme.
    Falla silenciosamente si no encuentra los archivos.
    """
    # Lógica de extracción de versión y parchado (ya existente)
    pass

if __name__ == "__main__":
    # Mantener soporte para ejecución manual si el usuario lo desea
    auto_sync_theme(DEFAULT_GAME_DIR, DEFAULT_THEME_DIR)
```

### [MODIFY] `src/bot_main.py` (o `main_gui.py`)
Agregaremos el "Pre-Flight Check" justo antes de inicializar el orquestador principal.

```python
from scripts.installer import auto_sync_theme
import logging

logger = logging.getLogger(__name__)

def pre_flight_checks():
    """Ejecuta rutinas de mantenimiento previas al arranque."""
    logger.info("[⚙️] Validando versión del Theme...")
    try:
        # Rutas dinámicas basadas en config.json
        auto_sync_theme(game_dir, theme_dir)
        logger.info("[✅] Theme sincronizado (Kanpeki).")
    except Exception as e:
        logger.error(f"[⚠️] Aviso: No se pudo auto-sincronizar el theme: {e}")

# Llamada en el bloque principal:
if __name__ == "__main__":
    pre_flight_checks()
    # arrancar_bot()...
```

## Verification Plan
### Automated Tests
1. No se requieren *frameworks* de test complejos. Se verificará modificando temporalmente el `info.xml` original.
### Manual Verification
1. Lanza el bot.
2. Observa la terminal PowerShell para confirmar el log `[✅] Theme sincronizado (Kanpeki).`.
3. Comprueba que el bot no haya demorado más de 0.5 segundos extra en arrancar.
