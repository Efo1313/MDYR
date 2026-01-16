import cloudscraper
import re
import os

def guncelle():
    # 1. Ayarlar
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    
    scraper = cloudscraper.create_scraper()
    
    try:
        # 2. Şifreyi (Token) Al
        print("Siteye giriş yapılıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        # Yönlendirilen son URL'den pass parametresini çek
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Şifre (pass) bulunamadı. Site yapısı değişmiş olabilir.")
            return
            
        token = token_match.group(1)
        print(f"Güncel Şifre Alındı: {token}")

        # 3. Kanalları Oku ve M3U Oluştur
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt dosyası bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        with open("liste.m3u", "w", encoding="utf-8") as m3u:
            m3u.write("#EXTM3U\n")
            
            for satir in kanallar:
                if ":" in satir:
                    kanal_adi, slug = satir.strip().split(": ")
                    # Tam linki oluştur: Worker + Site + Slug + Pass
                    final_link = f"{WORKER_URL}{BASE_URL}{slug}?pass={token}"
                    
                    m3u.write(f"#EXTINF:-1,{kanal_adi}\n")
                    m3u.write(f"{final_link}\n")
        
        print("İşlem Başarılı: liste.m3u güncellendi.")

    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

if __name__ == "__main__":
    guncelle()
