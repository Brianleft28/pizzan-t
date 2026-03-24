import cv2
import mss
import numpy as np

class PokéObserver:
    def __init__(self, region=None):
        self._sct = None
        self.region = region

    def capture_frame(self):
        """Captura la pantalla creando una instancia de mss por hilo para evitar errores de srcdc."""
        try:
            # mss no es thread-safe, necesitamos una instancia por hilo
            if self._sct is None:
                self._sct = mss.mss()

            if self.region:
                monitor = {
                    "top": self.region.get('y1', 0),
                    "left": self.region.get('x1', 0),
                    "width": self.region.get('x2', 1920) - self.region.get('x1', 0),
                    "height": self.region.get('y2', 1080) - self.region.get('y1', 0)
                }
            else:
                monitor = self._sct.monitors[1]

            sct_img = self._sct.grab(monitor)
            frame = np.array(sct_img)
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            # Si falla, reiniciamos el capturador para el siguiente intento
            self._sct = None
            print(f"Capture Error: {e}")
            return None
