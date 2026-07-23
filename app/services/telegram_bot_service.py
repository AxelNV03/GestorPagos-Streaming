import os
import requests

class BotService:
    
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN', '')
    WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID', '')
    
    @staticmethod
    def notificar_admin(mensaje):
        """Envía un mensaje al admin por Telegram"""
        try:
            url = f"https://api.telegram.org/bot{BotService.TOKEN}/sendMessage"
            data = {
                "chat_id": BotService.CHAT_ID,
                "text": mensaje,
                "parse_mode": "Markdown"
            }
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error Telegram: {e}")
            return False
    
    @staticmethod
    def enviar_whatsapp(telefono, mensaje):
        """Envía un mensaje de WhatsApp a un número"""
        try:
            url = f"https://graph.facebook.com/v17.0/{BotService.WHATSAPP_PHONE_ID}/messages"
            headers = {"Authorization": f"Bearer {BotService.WHATSAPP_TOKEN}"}
            data = {
                "messaging_product": "whatsapp",
                "to": telefono,
                "type": "text",
                "text": {"body": mensaje}
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error WhatsApp: {e}")
            return False