import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # 1. YAPILANDIRMA
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 2. GÜNCEL PASAPORTU (TOKEN) ÇEK
        print("Siteye giriş yapılıyor, güncel pasaport alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Pasaport kodu bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"Başarılı! Pasaport: {token[:10]}...")

        # 3. KANALLARI İŞLE VE AYRI DOSYALAR OLUŞTUR
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            if ":" in satir:
                kanal_adi, slug = satir.strip().split(": ")
                kanal_id = slug.replace("-online", "")
                
                # Link Oluşturma
                ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                final_link = f"{WORKER_URL}{karakterli_ic_link}"
                
                # Dosya adını düzenle
                dosya_adi = kanal_adi.replace(" ", "_") + ".m3u"
                dosya_yolu = os.path.join(KLASOR_ADI, dosya_adi)
                
                # Dosya içeriğini yaz (İstediğin formatta)
                with open(dosya_yolu, "w", encoding="utf-8") as f_m3u8:
                    f_m3u8.write("#EXTM3U\n") # Başlık
                    f_m3u8.write(f"{final_link}\n") # Link
                
                print(f"-> {dosya_adi} oluşturuldu.")
        
        print(f"\nTüm dosyalar '{KLASOR_ADI}' klasöründe hazır!")

    except Exception as e:
        print(f"Beklenmedik bir hata: {e}")

if name == "main":
    guncelle()
