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

    # Klasörün oluşturulacağı tam yolu al
    mevcut_dizin = os.getcwd()
    klasor_yolu = os.path.join(mevcut_dizin, KLASOR_ADI)

    # 1. Klasörü Oluşturma Denemesi
    try:
        if not os.path.exists(klasor_yolu):
            os.makedirs(klasor_yolu)
            print(f"Klasör oluşturuldu: {klasor_yolu}")
        else:
            print(f"Klasör zaten var: {klasor_yolu}")
    except Exception as e:
        print(f"KLASÖR OLUŞTURMA HATASI: {e}")
        print("Dosyalar ana dizine yazılacak.")
        klasor_yolu = mevcut_dizin

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        # 2. Token Al
        print("Siteden anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        token_match = re.search(r'pass=([a-zA-Z0-9]{10,50})', response.text + response.url)

        if not token_match:
            print("HATA: Token alınamadı!")
            return
        token = token_match.group(1)
        print(f"GÜNCEL TOKEN: {token}")

        # 3. Kanalları Oku
        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} dosyası bu konumda yok: {mevcut_dizin}")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        sayac = 0
        for satir in satirlar:
            satir = satir.strip()
            if not satir or ":" not in satir: continue
            
            parca = satir.split(":", 1)
            kanal_adi = parca[0].strip()
            kanal_id = parca[1].strip().replace("-online", "")
            
            player_no = "12" if "hd" in kanal_id.lower() else "11"
            
            ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
            encoded_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{encoded_link}"
            
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_adi = f"{temiz_ad}.m3u8"
            tam_dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
            
            with open(tam_dosya_yolu, "w", encoding="utf-8") as f_tekil:
                f_tekil.write(final_link)
            
            print(f">> YAZILDI: {dosya_adi}")
            sayac += 1

        print(f"\nİŞLEM TAMAMLANDI! {sayac} dosya hazır.")

    except Exception as e:
        print(f"SİSTEM HATASI: {e}")

if __name__ == "__main__":
    guncelle()
