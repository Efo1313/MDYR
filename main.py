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
    ANA_LISTE_ADI = "TUM_KANALLAR.m3u"
    
    # GITHUB LOGO AYARI
    USER_NAME = "Efo1313" 
    REPO_NAME = "MDYR"
    LOGO_BASE_URL = f"https://raw.githubusercontent.com/{USER_NAME}/{REPO_NAME}/main/logos/"

    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        print("Siteden güncel token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Token bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"Başarılı! Token: {token}")

        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt dosyası yok!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        ana_liste_yolu = os.path.join(KLASOR_ADI, ANA_LISTE_ADI)
        
        with open(ana_liste_yolu, "w", encoding="utf-8") as f_main:
            f_main.write("#EXTM3U\n")
            
            for satir in kanallar:
                if ":" in satir:
                    kanal_adi, slug = satir.strip().split(": ")
                    kanal_id = slug.replace("-online", "")
                    
                    # 1. İÇ LİNKİ OLUŞTUR (Örneğindeki gibi ?player=11... yapısı)
                    ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                    
                    # 2. KARAKTERLİ HALE GETİR (URL ENCODING)
                    # safe='' kullanarak : / ? = karakterlerinin hepsini % koduna çeviriyoruz
                    karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                    
                    # 3. FİNAL LİNK (Senin örneğinle birebir aynı yapı)
                    final_link = f"{WORKER_URL}{karakterli_ic_link}"
                    
                    # LOGO YAPILANDIRMASI
                    logo_dosya_adi = kanal_adi.replace(" ", "_").lower() + ".png"
                    logo_url = f"{LOGO_BASE_URL}{logo_dosya_adi}"
                    
                    # M3U DOSYASINA YAZ
                    f_main.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                    f_main.write(f"{final_link}\n")
                    
                    print(f"-> {kanal_adi} eklendi.")
        
        print(f"\nİşlem Başarılı! Liste oluşturuldu: {ana_liste_yolu}")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    guncelle()
