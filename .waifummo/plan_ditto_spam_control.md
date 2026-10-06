## Plan de Mejora: Control del Spam de Captura (Ditto)

### [Goal Description] (目的 - Mokuteki)
El problema principal que descubriste es que el *delay* al presionar 'X' cuando el Ditto es atrapado era confuso y no había un parámetro claro para controlarlo en la configuración. 
El objetivo de este plan es **parametrizar el delay del spam de teclas** para que el usuario (*bebito*) tenga control total sobre qué tan rápido se limpia la UI superpuesta, garantizando que el OCR lea instantáneamente.

### Proposed Changes

#### [MODIFY] `config.json`
Añadir un parámetro explícito para controlar la velocidad del bucle (el *spam*).
```json
  "timing_ball_wait": 0.5,
  "timing_capture_settle": 2.5,
  "timing_capture_spam_delay": 0.1,  // <-- [NUEVO] Controla el delay del spam de X
```

#### [MODIFY] `src/modes/base.py`
Enlazar el nuevo parámetro al bucle de captura para que ya no esté "*hardcodeado*".
```python
    def _check_capture_result(self):
        ball_wait   = float(self.config.get("timing_ball_wait", 0.5))
        settle_time = float(self.config.get("timing_capture_settle", 2.5))
        spam_delay  = float(self.config.get("timing_capture_spam_delay", 0.1)) # <-- [NUEVO]

        self.log(f"⏳ Waiting {ball_wait}s for ball animation...", "DEBUG")
        time.sleep(ball_wait)

        for _ in range(60):
            if not self.bot.running:
                return False
                
            # ACTIVE POLLING: Destruimos ventanas emergentes
            self.controller._press('left', duration=0.02)
            self.controller._press('x', duration=0.02)
            self.controller._press('right', duration=0.02)
            self.controller._press('x', duration=0.02)
            
            fb = self.observer.capture_frame()
            m = self.bot.check_msg_area(fb)

            if m == "SUCCESS":
                self.log("🎉 Message read: CAUGHT!", "SUCCESS")
                time.sleep(settle_time)
                # Cerrar diálogos adicionales...
                return True
            
            # ... (código existente de FAILURE / MENU)

            time.sleep(spam_delay) # <-- [MODIFICADO] Ahora usa el parámetro
```

## Open Questions (質問 - Shitsumon)
1. **Cambios Estéticos**: Mencionaste que hiciste "cambios estéticos" y quieres dejar por defecto la plantilla que tienes ahora, además de "subirlo a git". ¿Quieres que revise algún archivo de interfaz (UI) en particular o integro este cambio de la lógica de captura primero y luego hacemos el *push* a GitHub?

## Verification Plan
1. Ejecutar el bot.
2. Atrapar un Ditto.
3. Cambiar `timing_capture_spam_delay` en `config.json` si se siente muy lento o muy rápido, y observar la diferencia sin tocar código.
