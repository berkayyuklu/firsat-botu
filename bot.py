import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_deals():
    # DonanımHaber'in daha basit ve hata vermeyen bir veri kaynağını kullanıyoruz
    url = "https://firsat-api.donanimhaber.com/v1/firsatlar?sayfa=1&adet=5"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json() # Veriyi JSON olarak alıyoruz (daha güvenli)
        
        firsatlar = data.get('firsatlar', [])
        
        if not firsatlar:
            send_telegram("Şu an yeni fırsat bulunamadı.")
            return

        for firsat in firsatlar[:3]: # En yeni 3 fırsat
            baslik = firsat.get('baslik')
            link = "https://www.donanimhaber.com" + firsat.get('url')
            fiyat = firsat.get('fiyat', 'Fiyat belirtilmemiş')
            
            msg = f"🔥 **SICAK FIRSAT**\n\n📦 {baslik}\n💰 Fiyat: {fiyat}\n\n🔗 [Ürünü Gör]({link})"
            send_telegram(msg)
            
    except Exception as e:
        # Hata olursa ne olduğunu Telegram'dan görelim
        send_telegram(f"Sistemde bir aksama oldu: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    get_deals()
