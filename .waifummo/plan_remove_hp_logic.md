# Plan: Eliminación de Lógica de HP y Swap de Pokémon

## Objetivos
1. **Remover `read_hunter_hp` (OCR)**: Eliminar la función en `src/bot_main.py` que intenta leer el HP del cazador mediante OCR, ya que falla con barras verdes y da falsos 0.
2. **Remover `use_potion_sequence`**: Eliminar la secuencia en `src/controller.py` que abre el menú y selecciona el Pokémon (`_press('z')`), ya que al usar Smeargle de forma exclusiva, nunca es necesario cambiar Pokémon ni curarlo en combate de esta forma.
3. **Limpieza General**: Asegurarnos de que no quede ningún código fantasma que intente triggerear curaciones de HP o cambios de Pokémon.

## Archivos a Modificar
- `src/bot_main.py`: Eliminar def `read_hunter_hp`.
- `src/controller.py`: Eliminar def `use_potion_sequence`.

## Estado Actual
He revisado el código a fondo y he confirmado que la lógica de lectura de HP del cazador existe en estas funciones. Al eliminarlas, el bot dejará de intentar curar o cambiar a Smeargle por falsos positivos del OCR.

## Siguientes Pasos
Una vez apruebes el plan, ejecutaré los borrados y haré el commit en el repositorio.
