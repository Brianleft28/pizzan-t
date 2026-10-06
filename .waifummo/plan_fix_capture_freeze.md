# Plan: Fix Capture Freeze (El bot se "para")

## Goal Description
El usuario indicó que después de lanzar la Pokéball ("Throwing Ball"), el bot se "para" o congela.
Esto ocurre porque la lógica de "Active Polling" en `_check_capture_result` está apretando la tecla `X` *antes* de sacar la captura de pantalla. En PokeMMO, apretar la `X` cierra el diálogo de captura al instante, por lo que el OCR nunca llega a leer "CAUGHT" o "BROKE". Al no leer nada, el bot asume que sigue cargando y se queda atrapado en el bucle de spam de `X` por más de 1 minuto entero, dando la impresión de que "se paró".

## Proposed Changes

### `src/controller.py`
#### [MODIFY] `src/controller.py`
Se añadirá la opción `trailing=True` a `def _press()` para poder desactivar la pausa gigante obligatoria al spamear botones en la animación de la ball.

```python
def _press(self, key, duration=None, trailing=True):
    pydirectinput.keyDown(key)
    if duration:
        time.sleep(duration)
    else:
        time.sleep(random.uniform(0.12, 0.22))
    pydirectinput.keyUp(key)
    if trailing:
        time.sleep(random.uniform(0.2, 0.35))
```

### `src/modes/base.py`
#### [MODIFY] `src/modes/base.py`
Se reestructurará el bucle `_check_capture_result` para que **primero** lea la pantalla y **luego** presione `X` para avanzar el texto, de modo que no borre el mensaje de captura antes de leerlo.

```python
for _ in range(60):
    if not self.bot.running:
        return False
        
    fb = self.observer.capture_frame()
    m = self.bot.check_msg_area(fb)

    if m == "SUCCESS":
        self.log("🏆 Message read: CAUGHT!", "SUCCESS")
        time.sleep(settle_time)
        return True

    if m == "FAILURE":
        self.log("❌ Ball broke free - retrying next turn.", "WARN")
        time.sleep(1.5)
        return False

    if self.bot.is_menu_ready(fb):
        return False

    # Avanzamos diálogos lentamente sin romper la velocidad
    self.controller._press('x', duration=0.05, trailing=False)
    time.sleep(spam_delay)
```

## Verification Plan
1. Ejecutar el script Python para aplicar el fix de lógica.
2. Hacer push a GitHub para que puedas actualizar.
