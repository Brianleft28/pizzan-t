# Plan: Fix Leppa Healing & Version Bump

## Goal Description
El usuario reportó que el bot no está curando correctamente los PPs con las bayas Leppa después de los cambios de velocidad. El registro muestra que la secuencia se ejecuta muy rápido, lo que indica que el juego no llega a registrar la apertura de los menús (Party Menu y Move Menu) debido a delays excesivamente bajos. Además, se solicitó actualizar la versión del bot a `v7.0` y hacer push.

## Proposed Changes

### `src/controller.py`
Se aumentarán los tiempos mínimos de espera en las transiciones de menús pesados dentro de `use_leppa_sequence_single` para darle tiempo al juego de renderizar las opciones, pero manteniendo el toque humano aleatorio.

**Ajustes específicos:**
- Apertura del menú de Party (después del hotkey): `random.uniform(0.3, 0.8)` -> `random.uniform(0.6, 1.0)`
- Apertura de lista de movimientos (después de Z): `random.uniform(0.3, 0.8)` -> `random.uniform(0.6, 1.0)`
- Apertura del submenú de cantidad (después de elegir el ataque): `random.uniform(0.2, 0.6)` -> `random.uniform(0.5, 0.8)`
- Las micro-navegaciones (arriba/abajo/derecha) pueden mantenerse rápidas (`0.1` a `0.25`).

### `src/bot_main.py`
#### [MODIFY] `src/bot_main.py`
Se actualizará el banner de inicio del bot:
```python
# ANTES
self.logger.log("  THE HUMANOID HUNTER v6.9 - SENTINEL ", "SUCCESS")

# DESPUES
self.logger.log("  THE HUMANOID HUNTER v7.0 - SENTINEL ", "SUCCESS")
```

## Verification Plan
1. Ejecutar un script para reemplazar los tiempos problemáticos en `src/controller.py`.
2. Actualizar `bot_main.py` con la nueva versión.
3. Commit con la nomenclatura adecuada (`fix(leppa): increase menu render delays`) y push al repositorio.
