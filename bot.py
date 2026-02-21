import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_finance():
    # Alternatif ve daha stabil bir kaynak
    url = "https://finans.truncgil.com/today.json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Verileri güvenli çekme yöntemi (Hata vermez, veri yoksa '---' yazar)
        def v(key):
            return data.get(key, {}).get('Alış', '---')

        dolar = v('USD')
        euro = v('EUR')
        # Bazı servislerde isimler farklı olabiliyor, ikisini de kontrol edelim
        gram = v('Gram Altın') if v('Gram Altın') != '---' else v('GA')
        ceyrek = v('Çeyrek Altın') if v('Çeyrek Altın') != '---' else v('C')
        
        mesaj = (
            f"💰 **Finans Verileri**\n\n"
            f"💵 Dolar: {dolar} TL\n"
            f"💶 Euro: {euro} TL\n"
            f"🟡 Gram: {gram} TL\n"
            f"🪙 Çeyrek: {ceyrek} TL"
        )
        
        send_telegram(mesaj)
        
    except Exception as e:
        send_telegram(f"Veri çekme hatası: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_finance()
