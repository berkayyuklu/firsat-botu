import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_finance():
    # Bu kaynak altın ve dövizde çok daha kararlıdır
    url = "https://api.genelpara.com/embed/para-birimleri.json"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Verileri doğrudan çekiyoruz
        dolar = data.get('USD', {}).get('alis', '---')
        euro = data.get('EUR', {}).get('alis', '---')
        gram = data.get('GA', {}).get('alis', '---')
        ceyrek = data.get('C', {}).get('alis', '---')
        
        mesaj = (
            f"💰 **GÜNCEL FİNANS VERİLERİ**\n\n"
            f"💵 **Dolar:** {dolar} TL\n"
            f"💶 **Euro:** {euro} TL\n"
            f"🟡 **Gram Altın:** {gram} TL\n"
            f"🪙 **Çeyrek Altın:** {ceyrek} TL"
        )
        
        send_telegram(mesaj)
        
    except Exception as e:
        send_telegram("Veri şu an çekilemiyor, kaynak hatası.")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_finance()
