import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # --- AYARLAR ---
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    KANAL_DOSYASI = "kanallar.txt"

    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        print("Siteden güncel anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        if not token_match:
            print("Hata: Token alınamadı!")
            return
        token = token_match.group(1)

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            satir = satir.strip()
            if not satir or ":" not in satir: continue
            
            parca = satir.split(":", 1)
            kanal_adi = parca[0].strip()
            slug = parca[1].strip()
            kanal_id = slug.replace("-online", "")
            
            # Link oluşturma
            ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
            encoded_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{encoded_link}"
            
            # Dosya adını temizle ve oluştur
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u")
            
            # --- KRİTİK NOKTA: M3U FORMATINDA YAZ ---
            with open(dosya_yolu, "w", encoding="utf-8") as f_out:
                f_out.write("#EXTM3U\n") # Oynatıcının tanıması için şart!
                f_out.write(final_link) 
            
            print(f"Başarıyla hazırlandı: {temiz_ad}.m3u")

        print("\nİşlem tamam! Şimdi bu dosyaları GitHub'a yükle ve Peugeot dosyanı dene.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    guncelle()
