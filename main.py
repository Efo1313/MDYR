import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # 1. YAPILANDIRMA
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID=" # HTTPS olarak sabitlendi
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 2. GÜNCEL PASAPORTU (TOKEN) ÇEK
        print("Siteye giriş yapılıyor, güncel pasaport alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        # URL içindeki pass= parametresini yakala
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Pasaport kodu bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"Başarılı! Pasaport: {token[:15]}...")

        # 3. KANALLARI İŞLE VE DOSYALARI OLUŞTUR
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            if ":" in satir:
                kanal_adi, slug = satir.strip().split(": ")
                # Slug'dan kanal ID'sini temizle (Örn: bnt-4-online -> bnt-4)
                kanal_id = slug.replace("-online", "")
                
                # ÇALIŞAN FORMAT OLUŞTURMA:
                # İç linki hazırla
                ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                
                # İç linki URL Encode işleminden geçir (karakterli yap)
                # safe='' parametresi tüm karakterleri kodlamasını sağlar
                karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                
                # Worker URL ile birleştir
                final_link = f"{WORKER_URL}{karakterli_ic_link}"
                
                # Dosya adını hazırla ve kaydet (Boşlukları alt tire yapar)
                dosya_adi = kanal_adi.replace(" ", "_") + ".m3u"
                dosya_yolu = os.path.join(KLASOR_ADI, dosya_adi)
                
                with open(dosya_yolu, "w", encoding="utf-8") as f_m3u:
                    f_m3u.write(final_link)
                
                print(f"-> {dosya_adi} oluşturuldu.")
        
        print("\nTüm çalma listeleri 'playlist' klasöründe başarıyla güncellendi!")

    except Exception as e:
        print(f"Beklenmedik bir hata: {e}")

if __name__ == "__main__":
    guncelle()
