import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Amazon Fırsatları (Örnek: Çok Satanlar)
URL = "https://www.amazon.com.tr/gp/bestsellers/computers/ref=zg_bs_nav_computers_0"

def check_deals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        print(f"Site Yanıt Kodu: {response.status_code}")
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Amazon ürün kutularını bulalım
        products = soup.find_all("div", {"id": "gridItemRoot"})
        
        if not products:
            send_telegram("⚠️ Amazon'da ürün bulunamadı, kodun güncellenmesi gerekebilir.")
            return

        for product in products[:3]:
            name = product.find("div", {"class": "_cDE31_pbc-content_rdur2"}).text.strip()[:50] + "..."
            link = "https://www.amazon.com.tr" + product.find("a", {"class": "a-link-normal"})["href"]
            
            send_telegram(f"🔥 **Amazon Fırsatı!**\n\n📦 {name}\n🔗 [Ürüne Git]({link})")
            
    except Exception as e:
        print(f"Hata: {e}")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_deals()
