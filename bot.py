import requests
import os
import re

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_finance_data():
    # Döviz ve Altın verilerini engelsiz bir kaynaktan çekiyoruz
    url = "https://finans.truncgil.com/today.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Verileri ayıklıyoruz
        dolar = data.get('USD', {}).get('Alış', 'Hata')
        euro = data.get('EUR', {}).get('Alış', 'Hata')
        gram_altin = data.get('Gram Altın', {}).get('Alış', 'Hata')
        ceyrek_altin = data.get('Çeyrek Altın', {}).get('Alış', 'Hata')
        guncelleme = data.get('Update_Date', 'Bilinmiyor')

        mesaj = (
            f"💰 **Günlük Finans Özeti**\n"
            f"📅 {guncelleme}\n\n"
            f"🇺🇸 **Dolar:** {dolar} TL\n"
            f"🇪🇺 **Euro:** {euro} TL\n"
            f"🟡 **Gram Altın:** {gram_altin} TL\n"
            f"🪙 **Çeyrek Altın:** {ceyrek_altin} TL"
        )
        
        send_telegram(mesaj)
        
    except Exception as e:
        send_telegram(f"Finans verisi çekilirken hata oluştu: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_finance_data()
