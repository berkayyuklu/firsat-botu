import requests
import os
import xml.etree.ElementTree as ET

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_deals():
    # Bu adres botlara özeldir, engellenmesi çok zordur
    url = "https://www.donanimhaber.com/rss/sicakfirsatlar"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        # XML formatındaki veriyi okuyoruz
        root = ET.fromstring(response.content)
        
        # En yeni 3 ürünü alıyoruz
        items = root.findall("./channel/item")[:3]
        
        if not items:
            send_telegram("Şu an yeni fırsat akışı boş.")
            return

        for item in items:
            title = item.find("title").text
            link = item.find("link").text
            
            msg = f"🔥 **SICAK FIRSAT**\n\n📦 {title}\n\n🔗 [Ürünü Gör]({link})"
            send_telegram(msg)
            
    except Exception as e:
        send_telegram(f"Sistem hatası: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_deals()
