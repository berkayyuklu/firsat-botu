import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def test_connection():
    print(f"Sistem Kontrol Ediliyor...")
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    r = requests.get(url).json()
    
    if r.get("ok"):
        print(f"✅ Bot Baglantisi Basarili: {r['result']['username']}")
        
        # Mesaj gondermeyi dene
        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": "🚀 Test mesaji geliyor!"}
        response = requests.post(send_url, json=payload).json()
        
        if response.get("ok"):
            print("✅ Mesaj basariyla gonderildi!")
        else:
            print(f"❌ Mesaj gonderilemedi! Hata: {response.get('description')}")
    else:
        print("❌ Bot Token hatali! GitHub Secrets kismini kontrol et.")

if __name__ == "__main__":
    test_connection()
