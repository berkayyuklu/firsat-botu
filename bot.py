import requests
import os
import re

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_deals():
    # DonanımHaber Sıcak Fırsatlar (Dış kütüphane gerektirmeyen yöntem)
    url = "https://www.donanimhaber.com/rss/sicakfirsatlar"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        # XML içinden başlıkları ve linkleri basitçe cımbızla çekiyoruz (Regex)
        titles = re.findall('<title><!\[CDATA\[(.*?)\]\]></title>', response.text)
        links = re.findall('<link>(.*?)</link>', response.text)

        # İlk 3 tanesini gönder (İlk başlık genelde site adıdır, o yüzden 1'den başlıyoruz)
        for i in range(1, 4):
            msg = f"🔥 **FIRSAT:** {titles[i]}\n\n🔗 {links[i]}"
            send_telegram(msg)
            
    except Exception as e:
        send_telegram(f"Hata oluştu: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_deals()
