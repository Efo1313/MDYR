import cloudscraper
import re
import os
import urllib.parse
import time

def dosya_adi_temizle(metin):
    return re.sub(r'[\\/*?:"<>|]', "", metin).strip().replace(" ", "_")

def guncelle():
    KLASOR_ADI = "playlist"
    WORKER_URL = "http://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
    )
    
    try:
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = [s.strip() for s in f.readlines() if ":" in s]

        for satir in kanallar:
            kanal_adi, slug = satir.split(": ")
            kanal_sayfa_url = f"{BASE_URL}{slug}"
            
            temiz_ad = dosya_adi_temizle(kanal_adi)
            dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u")
            
            print(f"Güncelleniyor: {kanal_adi}")
            
            try:
                kanal_res = scraper.get(kanal_sayfa_url, timeout=10)
                token_match = re.search(r'pass=([a-zA-Z0-9]+)', kanal_res.text)
                
                if token_match:
                    token = token_match.group(1)
                    kanal_id = slug.replace("-online", "")
                    
                    # PLAYER 11 SEÇİLDİ ve Karakter Kodlaması Yapıldı
                    ham_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                    guvenli_link = urllib.parse.quote(ham_link, safe='')
                    final_url = f"{WORKER_URL}{guvenli_link}"
                    
                    # DOSYA İÇİNE SADECE ADRES YAZILIYOR
                    with open(dosya_yolu, "w", encoding="utf-8") as f_kanal:
                        f_kanal.write(final_url)
                    
                    print(f"-> {temiz_ad}.m3u (Sadece Link) oluşturuldu.")
                else:
                    print(f"-> {kanal_adi} için şifre bulunamadı.")
                
                time.sleep(0.5)
                        
            except Exception as e:
                print(f"-> {kanal_adi} hatası: {e}")

        print(f"\nİşlem tamam! Dosyalar sadece saf adres içeriyor.")

    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    guncelle()
