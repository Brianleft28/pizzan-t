import cv2
import mss
import numpy as np

class PokéObserver:
    def __init__(self, region=None):
        self._sct = None
        # Si no hay región, usamos la pantalla completa por defecto
        self.region = region if region else {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

    @property
    def sct(self):
        # Inicialización perezosa: se crea en el hilo que lo llame
        if self._sct is None:
            self._sct = mss.mss()
        return self._sct

    def capture_frame(self):
        """Captura un frame y lo convierte a formato OpenCV (BGR)"""
        try:
            screenshot = self.sct.grab(self.region)
            frame = np.array(screenshot)
            # Convertir de BGRA a BGR
            return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        except Exception as e:
            # Si falla (por ejemplo, al cambiar de hilo), reiniciamos el capturador
            self._sct = None
            return None
