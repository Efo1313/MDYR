import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # --- AYARLAR ---
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    
    # Eskiden 'playlist' klasörüne yazıyordu, şimdi klasörsüz ana dizine yazdıralım 
    # ki nerede olduğu kesin görünsün.
    KLASOR_ADI = "playlist" 
    KANAL_DOSYASI = "kanallar.txt"

    # Klasör oluşturma (Eğer izin varsa)
    if not os.path.exists(KLASOR_ADI):
        try:
            os.makedirs(KLASOR_ADI)
            print(f"Klasör oluşturuldu: {KLASOR_ADI}")
        except:
            print("Klasör oluşturulamadı, dosyalar ana dizine yazılacak.")
            KLASOR_ADI = "." # Mevcut dizin

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        print("Siteden güncel anahtar alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        
        # Token yakalamayı garantiye alalım
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        
        if not token_match:
            print("HATA: Token (pass) bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"TOKEN: {token}")

        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} bulunamadı!")
            return
            
        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            satir = satir.strip()
            if not satir or ":" not in satir: continue
            
            parca = satir.split(":", 1)
            kanal_adi = parca[0].strip()
            kanal_id = parca[1].strip().replace("-online", "")
            
            # HD kanallarda player 12 kullanımı
            player_no = "12" if "hd" in kanal_id.lower() else "11"
            
            ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
            encoded_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{encoded_link}"
            
            # Dosya ismini temizle ve yolu belirle
            temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            tekil_dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u8")
            
            with open(tekil_dosya_yolu, "w", encoding="utf-8") as f_tekil:
                f_tekil.write(final_link)
            
            print(f"Yazıldı: {tekil_dosya_yolu}")

        print(f"\nİşlem bitti. Dosyalar '{KLASOR_ADI}' konumunda.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
