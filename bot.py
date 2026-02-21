import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SEHIR = "Istanbul" # Buraya istediğin şehri Türkçe karakter olmadan yazabilirsin

def get_weather():
    # Hava durumu verisi için ücretsiz ve engelsiz bir kaynak
    url = f"https://wttr.in/{SEHIR}?format=j1"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        current = data['current_condition'][0]
        temp = current['temp_C']
        desc = current['lang_tr'][0]['value'] if 'lang_tr' in current else current['weatherDesc'][0]['value']
        feels_like = current['FeelsLikeC']
        humidity = current['humidity']

        emoji = "☀️"
        if "rain" in desc.lower() or "yağmur" in desc.lower(): emoji = "🌧️"
        elif "cloud" in desc.lower() or "bulut" in desc.lower(): emoji = "☁️"
        elif "snow" in desc.lower() or "kar" in desc.lower(): emoji = "❄️"

        mesaj = (
            f"🌍 **{SEHIR} Hava Durumu**\n\n"
            f"{emoji} **Durum:** {desc}\n"
            f"🌡️ **Sıcaklık:** {temp}°C\n"
            f"🧥 **Hissedilen:** {feels_like}°C\n"
            f"💧 **Nem:** %{humidity}\n\n"
            f"🚀 İyi günler dilerim!"
        )
        
        send_telegram(mesaj)
        
    except Exception as e:
        send_telegram(f"Hava durumu çekilemedi: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_weather
