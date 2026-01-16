import requests
import re

def guncel_liste_olustur():
    url = "https://www.seir-sanduk.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Sayfadaki güncel pass değerini yakala
        match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if match:
            sifre = match.group(1)
            print(f"Sifre Bulundu: {sifre}")

            # 1. Şifreyi metin dosyası olarak sakla
            with open("sifre.txt", "w") as f:
                f.write(sifre)

            # 2. Otomatik M3U Kanal Listesi Oluştur
            # Buradaki kanal numaralarını ve isimlerini ihtiyacına göre çoğaltabilirsin
            m3u_icerik = f"#EXTM3U\n"
            m3u_icerik += f"#EXTINF:-1,Seir Sanduk TV 1\nhttps://www.seir-sanduk.com/live.php?channel=1&pass={sifre}\n"
            m3u_icerik += f"#EXTINF:-1,Seir Sanduk TV 2\nhttps://www.seir-sanduk.com/live.php?channel=2&pass={sifre}\n"
            m3u_icerik += f"#EXTINF:-1,Seir Sanduk TV 3\nhttps://www.seir-sanduk.com/live.php?channel=3&pass={sifre}\n"
            
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_icerik)
                
            print("liste.m3u ve sifre.txt dosyaları güncellendi.")
        else:
            print("Hata: Sayfada sifre bulunamadı.")

    except Exception as e:
        print(f"Hata olustu: {e}")

if __name__ == "__main__":
    guncel_liste_olustur()
