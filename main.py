import requests
from bs4 import BeautifulSoup
import re
import os

def guncel_sifreyi_getir():
    # Seir Sanduk ana sayfası
    url = "https://www.seir-sanduk.com/"
    
    # Gerçekçi bir tarayıcı başlığı (GitHub sunucularının engellenmemesi için)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    print("Siteye bağlanılıyor...")

    try:
        # Siteye istek gönder
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Sayfa kaynağında pass= şifresini ara (Genelde URL içinde veya JS değişkeninde olur)
        # Örnek yapı: pass=11kalAdKaAde11sF8F...
        match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if match:
            yeni_sifre = match.group(1)
            print(f"Başarılı! Yeni şifre bulundu: {yeni_sifre}")
            
            # Şifreyi 'sifre.txt' dosyasına kaydet (GitHub Actions bunu fark edip güncelleyecek)
            with open("sifre.txt", "w") as f:
                f.write(yeni_sifre)
            
            # Ayrıca tam linki de bir dosyaya yazalım (Yedek olarak)
            with open("link.txt", "w") as f:
                f.write(f"https://www.seir-sanduk.com/?pass={yeni_sifre}")
                
            print("Dosyalar güncellendi.")
            
        else:
            print("HATA: Sayfa kaynağında 'pass=' anahtarı bulunamadı.")
            # Site yapısı değişmişse sayfanın bir kısmını loglara yazdır (Hata ayıklama için)
            print("Sayfa içeriği kontrol ediliyor (ilk 200 karakter):", response.text[:200])

    except Exception as e:
        print(f"Bağlantı veya işlem hatası: {e}")

if __name__ == "__main__":
    guncel_sifreyi_getir()
