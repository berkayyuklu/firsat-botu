import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Takip etmek istediğin kategorinin linkini buraya koyabilirsin
URL = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98?siralama=coksatan" 

def check_deals():
    # Hepsiburada'nın bizi bot olarak engellememesi için tarayıcı taklidi yapıyoruz
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ürünleri bul (Hepsiburada yapı değiştirirse burası güncellenir)
        products = soup.find_all("li", {"class": "productListContent-zAP0Y5msy8SdbnEfjBca"})
        
        if not products:
            print("Ürün bulunamadı, site yapısı değişmiş olabilir.")
            return

        # Sadece ilk 3 ürünü gönderelim ki spam olmasın
        for product in products[:3]:
            name = product.find("h3").text.strip()
            link = "https://www.hepsiburada.com" + product.find("a")["href"]
            
            message = f"🛍️ **Günün Fırsatı!**\n\n📦 {name}\n\n🔗 [Ürünü İncele]({link})"
            send_telegram(message)
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_deals()
