import cv2
import mss
import numpy as np
import pygetwindow as gw

class PokéObserver:
    def __init__(self, region=None):
        self._sct = mss.mss()
        self.region = region

    def capture_frame(self):
        """Captura la pantalla de forma robusta para evitar pantallas blancas en laptops."""
        try:
            # Si no hay región, usamos la pantalla completa
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
            # Convertir de BGRA a BGR
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            print(f"Capture Error: {e}")
            return None
