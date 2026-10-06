## Fix: Eliminación de Movimientos Erráticos (Active Polling) 🎯

> [!NOTE] Contexto (La Posta)
> Che mi amor, tenés 100% de razón. El problema es que en la función de *Active Polling* (la que limpia la pantalla de los stats del Ditto para que el OCR lea "CAUGHT"), el bot estaba espameando `Left -> X -> Right -> X` cada 0.3 segundos.
> Cuando la batalla termina y el PJ vuelve al *overworld*, esos inputs direccionales (`Left` y `Right`) hacen que el personaje corra de lado a lado como un loco dando "vueltas en ejes random".

## Goal Description
Pulir la lógica de `_check_capture_result` para que **solo** utilice el botón `x` (Cancelar) como mecanismo de limpieza de UI. Esto evita cualquier buffer de movimiento direccional y mantiene al personaje totalmente quieto al terminar la captura.

## Proposed Changes

### [MODIFY] `src/modes/base.py`
Se limpiará el *Active Polling* dentro de la función `_check_capture_result`:

```python
        for _ in range(60):
            if not self.bot.running:
                return False
                
            # ACTIVE POLLING: Destruimos ventanas emergentes solo con 'x' (Cancelar).
            # Removimos left/right para que el PJ no de vueltas en el overworld.
            self.controller._press('x', duration=0.02)
            
            fb = self.observer.capture_frame()
            m = self.bot.check_msg_area(fb)

            if m == "SUCCESS":
                self.log("✨ Message read: CAUGHT!", "SUCCESS")
                time.sleep(settle_time)
                # Cerrar diálogos adicionales sin moverse
                for _ in range(8):
                    self.controller._press('z', duration=0.05)
                    self.controller._press('x', duration=0.05)
                    time.sleep(0.3)
                return True
            # ... resto del código ...
```

## Verification Plan
### Automated Tests
1. Se reemplazará el código en `base.py`.
### Manual Verification
1. Lanza el bot y entra en un encuentro.
2. Al tirar la Pokebola, verás en la consola `Waiting 0.5s for ball animation...`.
3. El personaje **ya no** se moverá hacia los costados ni dará vueltas cuando termine el encuentro o atrape al Pokémon. Se quedará plantado esperando el siguiente encuentro.
