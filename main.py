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

    # 1. Klasör Hazırlığı (Kesin çözüm için temizleyip açar)
    if os.path.exists(KLASOR_ADI):
        shutil.rmtree(KLASOR_ADI)
    os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        # 2. Güncel Token'ı Al
        print("Siteden anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        # Token'ı hem URL'den hem içerikten en geniş haliyle yakala
        token_match = re.search(r'pass=([a-zA-Z0-9]{10,50})', response.text + response.url)

        if not token_match:
            print("HATA: Token alınamadı!")
            return
        token = token_match.group(1)
        print(f"GÜNCEL TOKEN: {token}")

        # 3. Kanallar.txt Okuma
        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} dosyası bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        sayac = 0
        for satir in satirlar:
            satir = satir.strip()
            if not satir or ":" not in satir:
                continue
            
            # Senin listene özel ayırma (Split)
            parca = satir.split(":", 1) # Sadece ilk iki noktaya odaklan
            kanal_adi = parca[0].strip()
            # ID kısmındaki '-online' ekini temizle (site link yapısına göre)
            kanal_id = parca[1].strip().replace("-online", "")
            
            # Bazı kanallar (HD olanlar) player 12 ile daha iyi çalışabilir, 
            # ama genel yapı player 11'dir.
            player_no = "11"
            if "hd" in kanal_id.lower():
                player_no = "12" # HD kanalları otomatik player 12'ye yönlendirir
            
            # Linki Oluştur
            ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
            encoded_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{encoded_link}"
            
            # Dosya Adını Oluştur (BNT 1 HD.m3u8 gibi)
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u8")
            
            with open(dosya_yolu, "w", encoding="utf-8") as f_tekil:
                f_tekil.write(final_link)
            
            print(f">> OLUŞTURULDU: {dosya_yolu}")
            sayac += 1

        print(f"\nİŞLEM TAMAMLANDI!")
        print(f"- {sayac} adet kanal dosyası 'playlist' klasörüne yazıldı.")
        print("- BNT 1 HD ve diğer tüm liste güncellendi.")

    except Exception as e:
        print(f"BEKLENMEDİK HATA: {e}")

if __name__ == "__main__":
    guncelle()
