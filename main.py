import requests
import re

def guncel_sifreyi_bul():
    url = "https://www.seir-sanduk.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        content = response.text
        
        # 1. Yöntem: Linklerin içindeki pass parametresini ara (En yaygın olan)
        # Örnek: ?pass=12345abc
        match = re.search(r'pass=([a-zA-Z0-9]+)', content)
        
        # 2. Yöntem: Eğer üstteki bulamazsa, tırnak içindeki 32 karakterli karmaşık yapıları ara
        if not match:
            match = re.search(r'["\']([a-zA-Z0-9]{20,})["\']', content)

        if match:
            sifre = match.group(1)
            print(f"Sifre Tespit Edildi: {sifre}")
            
            with open("sifre.txt", "w") as f:
                f.write(sifre)
                
            # M3U Listesini daha esnek oluşturalım
            m3u_icerik = f"#EXTM3U\n#EXTINF:-1,Seir Sanduk Kanal 1\nhttps://www.seir-sanduk.com/live.php?channel=1&pass={sifre}"
            
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_icerik)
                
            print("Dosyalar güncellendi.")
        else:
            print("Hata: Sayfada geçerli bir şifre formatı bulunamadı.")
            # Hata analizi için sayfanın bir kısmını loglara basalım
            print("Sayfa özeti:", content[:500])

    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    guncel_sifreyi_bul()
