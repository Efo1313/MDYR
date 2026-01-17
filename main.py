import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # 1. Ayarlar
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 2. Uzun Pasaportu (Token) Al
        print("Pasaport alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Şifre bulunamadı.")
            return
            
        token = token_match.group(1)
        print(f"Güncel Şifre Alındı: {token[:10]}...")

        # 3. Kanalları Oku ve Karakterli Linkleri Oluştur
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            if ":" in satir:
                kanal_adi, slug = satir.strip().split(": ")
                kanal_id = slug.replace("-online", "")
                
                # ÇALIŞAN FORMATIN HAZIRLANMASI
                # Önce iç linki oluşturuyoruz
                ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                
                # Linki karakterli (encoded) hale getiriyoruz
                karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                
                # Worker ile birleştiriyoruz
                final_link = f"{WORKER_URL}{karakterli_ic_link}"
                
                # Dosya adını hazırla ve kaydet
                dosya_adi = kanal_adi.replace(" ", "_") + ".m3u"
                dosya_yolu = os.path.join(KLASOR_ADI, dosya_adi)
                
                with open(dosya_yolu, "w", encoding="utf-8") as f_m3u:
                    f_m3u.write(final_link)
                
                print(f"-> {dosya_adi} oluşturuldu.")
        
        print("\nİşlem Başarılı: Tüm dosyalar çalışan formata güncellendi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
