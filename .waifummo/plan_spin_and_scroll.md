# Plan: Eliminación de Giro Aleatorio y Fix de UI (Scroll Ditto)

## Goal Description
El usuario reportó que:
1. El personaje sigue girando sobre su propio eje.
2. La pestaña "Ditto" de la interfaz gráfica carece de un scroll horizontal, dificultando ver todas las configuraciones.

Tras investigar:
- **Giro (Spin):** En `src/modes/base.py` (líneas 175-178), durante el `_check_capture_result()`, existe un `ACTIVE POLLING` que spamea las teclas `left`, `x`, `right`, `x` repetidamente para limpiar cuadros de texto emergentes (stats, nuevos movimientos, etc.) y leer el mensaje de "CAUGHT". Cuando el bot detecta una captura o falla, si el combate ya cerró y el jugador volvió al mapa abierto, esos inputs de `left`/`right` hacen que el personaje gire.
- **Scroll GUI:** En `main_gui.py`, la tab `self.tab_ditto` es un frame común. Hay que envolver su contenido en un `ctk.CTkScrollableFrame(orientation="horizontal")`.

## Proposed Changes

### `src/modes/base.py`
#### [MODIFY] `src/modes/base.py`
Eliminar los inputs direccionales dentro de la fase de polling, dejando solo el botón `x` o un `x` espaciado para cerrar diálogos sin mover al personaje.
```python
            # ACTIVE POLLING: Destruimos ventanas emergentes de stats para que el OCR pueda ver el "CAUGHT"
            self.controller._press('x', duration=0.05)
            time.sleep(0.05)
            self.controller._press('x', duration=0.05)
```

### `main_gui.py`
#### [MODIFY] `main_gui.py`
Modificar `_build_ditto_tab` para inyectar un scroll frame.
```python
    def _build_ditto_tab(self):
        # Inyectar scroll frame horizontal
        self.ditto_scroll = ctk.CTkScrollableFrame(self.tab_ditto, orientation="horizontal")
        self.ditto_scroll.pack(fill="both", expand=True)
        tab = self.ditto_scroll
```

## User Review Required
No hay riesgos. Esto soluciona problemas visuales/mecánicos sin afectar la detección OCR.

## Verification Plan
1. Reemplazar código en los archivos afectados.
2. Hacer commit y push.
