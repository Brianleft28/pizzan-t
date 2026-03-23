import cv2
import numpy as np
import os
import easyocr

class PokéRecognizer:
    def __init__(self, assets_path="assets"):
        self.assets_path = assets_path
        # OCR en Español e Inglés
        self.reader = easyocr.Reader(['es', 'en'])
        
        # Template de estrella por si el OCR no lee bien el texto "Shiny"
        self.shiny_star_tpl = self._load_template("shiny_star.png")

    def _load_template(self, name):
        path = os.path.join(self.assets_path, name)
        if os.path.exists(path):
            return cv2.imread(path, 0)
        return None

    def analyze_slot(self, slot_img):
        """
        Analiza el recorte de un nombre.
        Retorna: { 'name': str, 'is_shiny': bool }
        """
        gray = cv2.cvtColor(slot_img, cv2.COLOR_BGR2GRAY)
        results = self.reader.readtext(gray)
        
        full_text = " ".join([res[1] for res in results])
        
        # Detección de Shiny por texto
        is_shiny = any(word in full_text.lower() for word in ["shiny", "variocolor", "vário", "vã¡rio", "vã rico"])
        
        # Respaldo por imagen (estrella)
        if not is_shiny and self.shiny_star_tpl is not None:
            res_s = cv2.matchTemplate(gray, self.shiny_star_tpl, cv2.TM_CCOEFF_NORMED)
            if np.max(res_s) > 0.8: is_shiny = True

        return {
            'name': full_text,
            'is_shiny': is_shiny
        }
