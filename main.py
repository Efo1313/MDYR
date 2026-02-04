import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KANAL_DOSYASI = "kanallar.txt"

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        print("Siteden anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        
        if not token_match:
            print("HATA: Token bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"TOKEN: {token}")

        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} dosyası yok!")
            return
            
        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            satir = satir.strip()
            if not satir or ":" not in satir: continue
            
            parca = satir.split(":", 1)
            kanal_adi = parca[0].strip()
            kanal_id = parca[1].strip().replace("-online", "")
            
            player_no = "12" if "hd" in kanal_id.lower() else "11"
            
            ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
            final_link = f"{WORKER_URL}{urllib.parse.quote(ic_link, safe='')}"
            
            # KLASÖRÜ KALDIRDIK: Doğrudan ana dizine yazıyoruz
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_adi = f"{temiz_ad}.m3u8"
            
            with open(dosya_adi, "w", encoding="utf-8") as f_tekil:
                f_tekil.write(final_link)
            
            print(f"DOSYA OLUŞTU: {dosya_adi}")

        print("\nİşlem bitti. Sayfayı yenileyip kontrol et.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
