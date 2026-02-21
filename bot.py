import requests
import xml.etree.ElementTree as ET
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Engellenmeyen, bot dostu bir indirim kaynağı (RSS)
RSS_URL = "https://www.donanimhaber.com/rss/sicakfirsatlar"

def check_deals():
    try:
        response = requests.get(RSS_URL)
        # XML verisini parçalıyoruz
        root = ET.fromstring(response.content)
        
        # En yeni 3 fırsatı çekelim
        items = root.findall("./channel/item")[:3]
        
        for item in items:
            title = item.find("title").text
            link = item.find("link").text
            
            message = f"🔥 **SICAK FIRSAT!**\n\n📦 {title}\n\n🔗 [Detaylar ve Ürün için Tıkla]({link})"
            send_telegram(message)
            
    except Exception as e:
        print(f"Hata: {e}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_deals()
