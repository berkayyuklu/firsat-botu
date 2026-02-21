import requests
from bs4 import BeautifulSoup
import os

# Şifreleri GitHub Secrets'tan çekiyoruz
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = "https://www.hepsiburada.com/laptop-notebook-dizustu-bilgisayarlar-c-98" 

def check_deals():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Hepsiburada'nın ürün listesini buluyoruz
    products = soup.find_all("li", {"class": "productListContent-zAP0Y5msy8SdbnEfjBca"})
    
    if products:
        product = products[0] # İlk ürünü alalım deneme için
        name = product.find("h3").text
        link = "https://www.hepsiburada.com" + product.find("a")["href"]
        
        message = f"✅ Bot Çalışıyor!\n\n📦 Bulunan Ürün: {name}\n🔗 {link}"
        send_telegram(message)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_deals()
