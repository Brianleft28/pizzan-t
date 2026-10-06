## Fix: Warnings del Auto-Updater 🛠️

> [!NOTE] Contexto (La Posta)
> ¡Tenés toda la razón, mi amor! Me saltó la térmica y no me di cuenta de dos cosas clave en tu máquina:
> 1. Tu PokeMMO está instalado en `C:\Program Files\PokeMMO` (y el script no estaba buscando ahí).
> 2. El juego no guarda su versión en `default/info.xml` como yo pensaba, sino en un archivo llamado `revision.txt` en la raíz del juego.
> Por eso te saltan los *warnings* (el script falla silenciosamente como debe, pero igual te avisa que no pudo hacer su magia).

## Goal Description
Modificar la lógica de *scraping* del tema para que busque en la ruta correcta y lea la versión directamente de `revision.txt`, silenciando así los *warnings* y logrando que el *auto-updater* funcione de manera *god* y sin joderte la consola.

## Proposed Changes

### [MODIFY] `scripts/installer.py`
Se actualizará la lógica interna de la función `auto_sync_theme`:

```python
    if not pokemmo_dir:
        # Añadida tu ruta real a la lista de búsqueda
        common_paths = [
            "C:\\Program Files\\PokeMMO",
            "C:\\PokeMMO",
            "D:\\PokeMMO",
            os.path.expanduser("~\\Desktop\\PokeMMO")
        ]
        # ...
        
    # Extraer versión del juego desde revision.txt
    revision_path = os.path.join(pokemmo_dir, "revision.txt")
    if not os.path.exists(revision_path):
        logger.warning("[⚠️] Auto-Sync: No se encontró revision.txt.")
        return False

    try:
        with open(revision_path, "r", encoding="utf-8") as f:
            current_version = f.read().strip()
    except Exception:
        return False
```

## Verification Plan
### Automated Tests
1. Se correrá el script localmente simulando el arranque. Al leer el `revision.txt`, extraerá el valor (ej. `32920`) y lo inyectará en el `info.xml` de *PizzantTheme*.
### Manual Verification
1. Cuando arranques `main_gui.py`, ya no te saldrán los *warnings* amarillos de "Directorio no encontrado" o "No se encontró el info.xml". Te saldrá directamente un mensajito verde: `[✅] Theme Pizzant auto-sincronizado con versión PokeMMO.`
