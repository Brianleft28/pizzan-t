# Post-Mortem y Arquitectura: Migración del PizzaTheme a Mod (TWL Engine)

## El Problema Original
PokeMMO rechazaba el tema cargado desde la carpeta `data/themes/pizzatheme` porque mezclaba sintaxis moderna con el modo legacy, provocando un crasheo del motor TWL. 
Se requirió empaquetar el tema en formato Mod (`PizzaTheme.mod`).

## La Secuencia de Bugs (Efecto Dominó)
Al migrar el tema a formato Mod, ocurrieron tres problemas críticos:

1. **Mod Invisible (Falta de icon.png y estructura XML interna)**:
   - *Causa*: El script `build_mod.py` filtraba y eliminaba el archivo `info.xml` interno de la carpeta `pizzatheme/` dentro del ZIP. El Mod Manager de PokeMMO requiere que todo `<theme>` declarado en el XML raíz del Mod posea su propio `info.xml` dentro del subdirectorio especificado (`path="pizzatheme"`). Además, el icono del mod no se estaba copiando a la raíz.
   - *Solución*: Se dejó de filtrar `info.xml` y se copió `icon.png` directamente a la raíz del `.mod`.

2. **Rechazo por Engine Revision (Error de compatibilidad futuro)**:
   - *Causa*: El archivo `info.xml` del Mod definía `<themes theme_revision="9">`. Al inspeccionar los logs del juego (`mods.log`), se descubrió el siguiente error crítico:
     `[ERROR] - Theme revision 9 is above current revision 8: PizzaTheme.mod`
   - *Solución*: Se hizo un downgrade de la metadata en `build_mod.py` para forzar `theme_revision="8"`, coincidiendo exactamente con la versión del cliente de PokeMMO actual.

## Instalador Unificado (`instalar_pizza_theme.bat`)
Para facilitar la sincronización en arquitecturas Multi-PC (Gamer vs Work), todo este flujo se consolidó en un único archivo Batch.
Este instalador:
1. Detecta automáticamente la ruta del PokeMMO.
2. Elimina la instalación obsoleta/corrupta en `data/themes/pizzatheme` para evitar conflictos.
3. Llama a `scripts/build_mod.py` para empaquetar el Mod con la revisión y XML correctos.
4. Mueve automáticamente el `.mod` a la carpeta `data/mods/`.

De esta forma, en cualquier PC nueva, el usuario simplemente hace `git pull` y ejecuta `instalar_pizza_theme.bat` (o el botón "SYNC PIZZA THEME" de la UI) para tener el mod perfectamente configurado.
