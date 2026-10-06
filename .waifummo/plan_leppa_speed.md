# Plan: Optimización de Velocidad en Menús y Combate

## Goal Description
El usuario solicitó acelerar todas las secuencias de `time.sleep()` dentro de `src/controller.py`, no solo para curar PP (`use_leppa_sequence_single`) sino también para las secuencias de combate (`open_fight_menu`, `use_ball`, `run_away`, `navigate_and_confirm_move`, etc.). Además, pidió que los valores sean variables entre un rango rápido como `0.1` a `1.2` segundos para evitar la detección del macro y acelerar el farmeo.

## Proposed Changes

### `src/controller.py`
Vamos a reemplazar los `time.sleep` estáticos por valores generados con `random.uniform()`.
Además, existe un método `_human_wait(min_s, max_s)` que puede ser utilizado en lugar de importar random en cada lugar, o podemos usar directamente `time.sleep(random.uniform(...))`. 

**Secuencias a acelerar:**
- **`use_leppa_sequence_single`**: Acelerar los sleeps de 1.0, 0.8 y 0.4.
- **`use_leppa_sequence`**: Acelerar la secuencia masiva de curación.
- **`use_ball`**: Bajar tiempos fijos para lanzar balls más rápido.
- **`open_fight_menu` / `execute_move`**: Hacer que los clics en el menú de pelea sean casi instantáneos (ej. 0.1s a 0.2s) en lugar de largos.
- **`run_away`**: Optimizar el tiempo de escape.
- **`use_sweet_scent`**: Acelerar la apertura de la mochila y uso de dulce aroma.

### Ejemplo de ajustes:
- `time.sleep(1.0)` -> `time.sleep(random.uniform(0.4, 0.8))`
- `time.sleep(0.4)` -> `time.sleep(random.uniform(0.15, 0.3))`
- `time.sleep(2.0)` (Animaciones) -> `time.sleep(random.uniform(1.2, 1.5))`

## Verification Plan
1. Reemplazar los valores en `src/controller.py`.
2. Documentar los cambios.
3. Hacer `git add`, `git commit` y `git push` para que los archivos estén listos en GitHub para ser clonados.
