import requests
from bs4 import BeautifulSoup
import re

def guncel_sifreyi_getir():
    # Seir Sanduk ana sayfası
    url = "https://www.seir-sanduk.com/"
    
    # Gerçekçi bir tarayıcı başlığı
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("Siteye bağlanılıyor...")

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Sayfadaki şifreyi (pass=...) bul
        match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if match:
            yeni_sifre = match.group(1)
            print(f"Başarılı! Yeni şifre: {yeni_sifre}")
            
            # Şifreyi GitHub'ın kaydedebileceği dosyaya yaz
            with open("sifre.txt", "w") as f:
                f.write(yeni_sifre)
            
            # Tam linki de yedek olarak yaz
            with open("link.txt", "w") as f:
                f.write(f"https://www.seir-sanduk.com/?pass={yeni_sifre}")
                
            print("Dosyalar başarıyla oluşturuldu.")
        else:
            print("HATA: Sayfada 'pass=' anahtarı bulunamadı!")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    guncel_sifreyi_getir()
