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
            
            print(f"Tarama Başladı: {kanal_adi}")
            
            try:
                response = scraper.get(kanal_sayfa_url, timeout=15)
                html_icerik = response.text

                # 1. STRATEJİ: pass= sonrasındaki en uzun diziyi ara
                # 2. STRATEJİ: Tırnak içindeki 32-64 karakter arası karmaşık dizileri ara
                # 3. STRATEJİ: Gizli input veya JS değişkenlerini tara
                potansiyel_tokenlar = re.findall(r'[Pp]ass=["\']?([a-zA-Z0-9]{20,})', html_icerik)
                genel_uzun_diziler = re.findall(r'["\']([a-zA-Z0-9]{30,64})["\']', html_icerik)
                
                tum_adaylar = potansiyel_tokenlar + genel_uzun_diziler
                
                if tum_adaylar:
                    # En uzun ve karmaşık görüneni seçiyoruz (Gerçek pasaport budur)
                    token = max(tum_adaylar, key=len)
                    kanal_id = slug.replace("-online", "")
                    
                    # PLAYER 11 + ENCODED
                    ham_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                    guvenli_link = urllib.parse.quote(ham_link, safe='')
                    final_url = f"{WORKER_URL}{guvenli_link}"
                    
                    temiz_ad = kanal_adi.replace(" ", "_")
                    dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u")
                    
                    with open(dosya_yolu, "w", encoding="utf-8") as f_kanal:
                        f_kanal.write(final_url)
                    
                    print(f"-> {kanal_adi} OK: {token[:10]}...")
                else:
                    print(f"-> {kanal_adi} için pasaport bulunamadı.")
                
                time.sleep(1.5) # Engellenmemek için süreyi biraz artırdık
                        
            except Exception as e:
                print(f"Hata ({kanal_adi}): {e}")

    except Exception as e:
        print(f"Sistem Hatası: {e}")

if __name__ == "__main__":
    guncelle()
