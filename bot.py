import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Kategori linki
URL = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98"

def check_deals():
    # Tarayıcı gibi görünmek için daha detaylı bilgiler ekledik
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(URL, headers=headers, timeout=15)
        print(f"Site Yanıt Kodu: {response.status_code}") # 200 ise sorun yok demektir
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ürünleri yakalamaya çalışıyoruz
        products = soup.find_all("li", {"class": "productListContent-zAP0Y5msy8SdbnEfjBca"})
        
        if not products:
            # Eğer ürün bulamazsa en azından botun yaşadığını haber ver
            send_telegram("⚠️ Bot çalıştı ama Hepsiburada ürün listesini vermedi. Site yapısı değişmiş olabilir.")
            return

        for product in products[:3]:
            try:
                name = product.find("h3").text.strip()
                link = "https://www.hepsiburada.com" + product.find("a")["href"]
                send_telegram(f"🛍️ **Yeni Fırsat!**\n\n📦 {name}\n🔗 [Ürüne Git]({link})")
            except:
                continue
                
    except Exception as e:
        send_telegram(f"❌ Bir hata oluştu: {str(e)}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_deals()
