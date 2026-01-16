import requests
from bs4 import BeautifulSoup
import re

def guncel_sifreyi_getir():
    # Seir Sanduk ana sayfası
    url = "https://www.seir-sanduk.com/"
    
    # Telefon tarayıcısı gibi görünmek için başlık (User-Agent)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
    }

    print("Siteye bağlanılıyor ve şifre aranıyor...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 1. Yöntem: Linklerin içindeki pass= parametresini ara
        # Örnek: ?pass=11kalAdKaAde11sF8F...
        match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if match:
            sifre = match.group(1)
            tam_link = f"https://www.seir-sanduk.com/?pass={sifre}"
            
            print("\n" + "="*30)
            print(f"BAŞARILI! GÜNCEL ŞİFRE: {sifre}")
            print(f"TAM LİNK: {tam_link}")
            print("="*30)
            print("\nBu linki kopyalayıp IPTV uygulamanıza (Televizo vb.) yapıştırabilirsiniz.")
            
        else:
            print("HATA: Sayfa içinde şifre bulunamadı. Site yapısı değişmiş olabilir.")

    except Exception as e:
        print(f"Bağlantı hatası oluştu: {e}")

if __name__ == "__main__":
    guncel_sifreyi_getir()
