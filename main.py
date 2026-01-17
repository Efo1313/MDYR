import cloudscraper
import re
import os
import urllib.parse
import time

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
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = [s.strip() for s in f.readlines() if ":" in s]

        for satir in kanallar:
            kanal_adi, slug = satir.split(": ")
            kanal_sayfa_url = f"{BASE_URL}{slug}"
            
            print(f"Güncelleniyor: {kanal_adi}")
            
            try:
                response = scraper.get(kanal_sayfa_url, timeout=15)
                
                # STRATEJİ: Sayfa içindeki en uzun 'pass' benzeri kod dizisini bul
                # Sadece pass= değil, tırnak içindeki 30-40 karakterli karmaşık kodları arıyoruz
                tokens = re.findall(r'pass=([a-zA-Z0-9]{20,})', response.text)
                
                if not tokens:
                    # Alternatif: Sayfa içinde tek başına duran uzun karmaşık dizileri ara
                    tokens = re.findall(r'["\']([a-zA-Z0-9]{30,})["\']', response.text)

                if tokens:
                    # Bulunanlar içinden en uzun olanı seç (Pasaport genellikle en uzunudur)
                    token = max(tokens, key=len)
                    kanal_id = slug.replace("-online", "")
                    
                    # PLAYER 11 ve TAM ENCODED YAPI
                    ham_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                    guvenli_link = urllib.parse.quote(ham_link, safe='')
                    final_url = f"{WORKER_URL}{guvenli_link}"
                    
                    temiz_ad = kanal_adi.replace(" ", "_")
                    dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u")
                    
                    with open(dosya_yolu, "w", encoding="utf-8") as f_kanal:
                        f_kanal.write(final_url)
                    
                    print(f"-> {kanal_adi} pasaportu yakalandı.")
                else:
                    print(f"-> {kanal_adi} için uygun pasaport bulunamadı.")
                
                time.sleep(1)
                        
            except Exception as e:
                print(f"Hata: {e}")

    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    guncelle()
