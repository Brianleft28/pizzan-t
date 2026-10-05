import threading
import requests
import json
import os

class WebhookNotifier:
    def __init__(self, bot):
        self.bot = bot
        self.log = bot.log

    def send_alert_async(self, category, message, img_path):
        url = self.bot.config.get("discord_webhook")
        jwt_token = self.bot.config.get("webhook_jwt", "").strip()
        
        if not url:
            self.log("Webhook URL no configurada. Saltando alerta.", "WARN")
            return
            
        self.log(f"Iniciando hilo para Webhook: {category}...", "INFO")
        thread = threading.Thread(
            target=self._send_payload, 
            args=(url, jwt_token, category, message, img_path),
            daemon=True
        )
        thread.start()

    def _send_payload(self, url, jwt_token, category, message, img_path):
        try:
            # Si hay un JWT configurado, asumimos que va al servidor NestJS
            if jwt_token:
                headers = {"Authorization": f"Bearer {jwt_token}"}
                payload = {
                    "category": category,
                    "message": message,
                    "encounters": str(self.bot.encounters)
                }
                
                if img_path and os.path.exists(img_path):
                    with open(img_path, "rb") as f:
                        files = {"file": (os.path.basename(img_path), f, "image/png")}
                        res = requests.post(url, headers=headers, data=payload, files=files, timeout=10)
                else:
                    res = requests.post(url, headers=headers, data=payload, timeout=10)
            
            # Retrocompatibilidad: Si no hay JWT, se envía como un embed directo a Discord
            else:
                payload = {
                    "payload_json": json.dumps({
                        "embeds": [{
                            "title": f"🚨 {category} DETECTED 🚨",
                            "description": f"**Status:** {message}\n**Total Encounters:** {self.bot.encounters}",
                            "color": 16766720, # Color dorado/Shiny
                            "thumbnail": {"url": "https://cdn-icons-png.flaticon.com/512/287/287221.png"},
                            "footer": {"text": "The Humanoid Hunter v7.0"}
                        }]
                    })
                }
                
                if img_path and os.path.exists(img_path):
                    with open(img_path, "rb") as f:
                        files = {"file": (os.path.basename(img_path), f, "image/png")}
                        res = requests.post(url, data=payload, files=files, timeout=10)
                else:
                    res = requests.post(url, data=payload, timeout=10)

            # Validar respuesta
            if res.status_code in [200, 201, 204]:
                self.log(f"✅ Webhook enviado con éxito ({res.status_code}).", "SUCCESS")
            else:
                self.log(f"⚠️ Error Webhook: {res.status_code} - {res.text}", "WARN")
                
        except Exception as e:
            self.log(f"❌ Fallo crítico al enviar Webhook: {e}", "FATAL")
