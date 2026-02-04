import cloudscraper
import re
import os
import urllib.parse
import shutil

def guncelle():
    # --- AYARLAR ---
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    KANAL_DOSYASI = "kanallar.txt"

    # 1. Klasörü Sıfırla (Geri gelmeme sorununu kökten çözer)
    if os.path.exists(KLASOR_ADI):
        print(f"Eski {KLASOR_ADI} klasörü temizleniyor...")
        shutil.rmtree(KLASOR_ADI) # Klasörü komple siler
    
    os.makedirs(KLASOR_ADI) # Klasörü tertemiz baştan açar
    print(f"'{KLASOR_ADI}' klasörü yeniden oluşturuldu.")

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        # 2. Token Al
        print("Siteden güncel anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        token_match = re.search(r'pass=([a-zA-Z0-9]{10,50})', response.text + response.url)

        if not token_match:
            print("HATA: Siteden 'pass' kodu alınamadı! İnternetini veya siteyi kontrol et.")
            return

        token = token_match.group(1)
        print(f"GÜNCEL TOKEN: {token}")

        # 3. Kanalları oku ve oluştur
        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} bulunamadı! Python dosyasının yanında bu dosya olmalı.")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()
            if not kanallar:
                print("UYARI: kanallar.txt dosyasının içi boş!")
                return

        for satir in kanallar:
            satir = satir.strip()
            if not satir or ":" not in satir: continue
            
            parca = satir.split(":")
            kanal_adi = parca[0].strip()
            kanal_id = parca[1].strip().replace("-online", "")
            player_no = parca[2].strip() if len(parca) > 2 else "11"
            
            ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
            encoded_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{encoded_link}"
            
            # Dosya adını temizle ve oluştur
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u8")
            
            with open(dosya_yolu, "w", encoding="utf-8") as f_tekil:
                f_tekil.write(final_link)
            
            print(f">> DOSYA YAZILDI: {dosya_yolu}")

        print("\n--- İŞLEM TAMAM ---")
        print(f"Lütfen şimdi '{KLASOR_ADI}' klasörüne gir ve BNT 1'i kontrol et.")

    except Exception as e:
        print(f"BEKLENMEDİK HATA: {e}")

if __name__ == "__main__":
    guncelle()
