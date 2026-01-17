import cloudscraper
import re
import os
import urllib.parse
import time

def guncelle():
    # YAPILANDIRMA
    KLASOR_ADI = "playlist"  # Dosyanın kaydedileceği klasör
    DOSYA_ADI = "liste.m3u"
    WORKER_URL = "http://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    
    # Klasör yoksa oluştur
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)
        print(f"'{KLASOR_ADI}' klasörü oluşturuldu.")

    KAYIT_YOLU = os.path.join(KLASOR_ADI, DOSYA_ADI)
    scraper = cloudscraper.create_scraper()
    
    try:
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        # Dosyayı belirlenen klasörün içine açıyoruz
        with open(KAYIT_YOLU, "w", encoding="utf-8") as m3u:
            m3u.write("#EXTM3U\n")
            
            for satir in kanallar:
                if ":" in satir:
                    kanal_adi, slug = satir.strip().split(": ")
                    kanal_sayfa_url = f"{BASE_URL}{slug}"
                    
                    print(f"Güncelleniyor: {kanal_adi}")
                    
                    try:
                        kanal_res = scraper.get(kanal_sayfa_url, timeout=15)
                        token_match = re.search(r'pass=([a-zA-Z0-9]+)', kanal_res.text)
                        
                        if token_match:
                            token = token_match.group(1)
                            kanal_id = slug.replace("-online", "")
                            
                            # Player 13 ve Güvenli Karakterli Link
                            ham_link = f"{BASE_URL}?player=13&id={kanal_id}&pass={token}"
                            guvenli_link = urllib.parse.quote(ham_link, safe='')
                            final_url = f"{WORKER_URL}{guvenli_link}"
                            
                            m3u.write(f"#EXTINF:-1,{kanal_adi}\n")
                            m3u.write(f"{final_url}\n")
                        else:
                            print(f"! {kanal_adi} için şifre bulunamadı.")
                            
                        time.sleep(1) # Siteyi bloklamamak için
                        
                    except Exception as e:
                        print(f"! {kanal_adi} hatası: {e}")

        print(f"\nİşlem tamam! Dosya şuraya kaydedildi: {KAYIT_YOLU}")

    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    guncelle()
