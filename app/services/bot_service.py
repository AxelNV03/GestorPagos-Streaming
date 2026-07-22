import os
import requests

class BotService:
    
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    
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