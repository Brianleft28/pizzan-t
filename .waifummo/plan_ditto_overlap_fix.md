## 🎯 Goal Description (El Problema del Overlap)

¡Tu descubrimiento es brillante, Brian Nahuel! Lo que está ocurriendo técnicamente se conoce como un **UI Overlap** (Superposición de Interfaz).
Cuando lanzas la Pokébola, el juego registra la captura, pero la ventana emergente de Ditto salta al **Foreground** (primer plano) y tapa físicamente las coordenadas del OCR que están en el **Background** (segundo plano). Como el bot solo se queda mirando (haciendo *Polling* pasivo), nunca logra leer el mensaje de "CAUGHT" y colapsa esperando.

**La Solución (*Kaiketsu* - 解決):**
Cambiaremos la función `_check_capture_result` de ser un observador pasivo a uno activo. El bot hará un *spam* (masheo) rápido de la tecla 'X' (y flechas para el *Input Focus*) **MIENTRAS** escanea la pantalla. Así, destruye la ventana del Ditto instantáneamente, revelando el texto debajo para que el OCR lea el éxito sin demoras.

---

## 🛠️ Proposed Changes

### `src/modes/base.py`

#### [MODIFY] `_check_capture_result`
Se inyectará el *spam* rápido de teclas directamente dentro del ciclo de lectura de los 60 intentos (*polls*).

```python
    def _check_capture_result(self):
        ball_wait   = float(self.config.get("timing_ball_wait", 0.5))
        settle_time = float(self.config.get("timing_capture_settle", 2.5))

        self.log(f"⏳ Waiting {ball_wait}s for ball animation...", "DEBUG")
        time.sleep(ball_wait)

        for _ in range(60):
            if not self.bot.running: return False
            
            # --- NUEVO: SPAM RÁPIDO PARA LIMPIAR OVERLAP DE UI ---
            # Presionamos flechas para recuperar el Input Focus y X para cerrar
            self.controller._press('left', duration=0.02)
            self.controller._press('x', duration=0.02)
            
            # Tomamos captura justo después de intentar limpiar la pantalla
            fb = self.observer.capture_frame()
            m = self.bot.check_msg_area(fb)

            if m == "SUCCESS":
                self.log("🎉 Message read: CAUGHT!", "SUCCESS")
                time.sleep(settle_time)
                # Spam final de seguridad por si quedaron diálogos
                for _ in range(10):
                    self.controller._press('x', duration=0.05)
                return True

            if m == "FAILURE":
                self.log("💨 Ball broke free — retrying next turn.", "WARN")
                time.sleep(1.5)
                return False

            if self.bot.is_menu_ready(fb):
                return False

            time.sleep(0.1) # Polling más rápido (100ms)

        self.log("⏱️ Capture check timed out after 60 polls.", "WARN")
        return False
```

### `src/controller.py` y `src/modes/single.py`
Se mantienen los ajustes previamente planificados:
* Micro-retrasos en `run_away()` para evitar que el lag se trague los inputs direccionales.
* Verificación doble de escape en `_wait_for_map()` para evitar el patrullaje accidental en batalla.

---

## 🚦 User Review Required
> [!IMPORTANT]
> **Aprobación del Plan de Overlap**
> Esta solución integra tus dos descubrimientos: el uso de las flechas para el *Input Focus* y la necesidad del *spam rápido* durante la lectura del OCR para despejar la pantalla. ¿Te parece que el código propuesto refleja exactamente tu idea?
