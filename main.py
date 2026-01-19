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
    ANA_LISTE_ADI = "TUM_KANALLAR.m3u"
    
    KANAL_DOSYASI = "kanallar.txt"
    LOGO_DOSYASI = "Tv logo.txt"

    # Klasör yoksa oluştur (Ana liste içine gidecek)
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 1. LOGO LİNKLERİNİ HAFIZAYA AL
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        # Boşlukları temizleyerek sözlüğe al (Tekrarı engeller)
                        parca = satir.strip().split(":", 1)
                        k_adi = parca[0].strip()
                        l_link = parca[1].strip()
                        logo_sozlugu[k_adi] = l_link

        # 2. TOKEN AL
        print("Siteden güncel token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        if not token_match:
            print("Hata: Token bulunamadı!")
            return
        token = token_match.group(1)

        # 3. KANALLARI OKU VE TEK LİSTE OLUŞTUR
        if not os.path.exists(KANAL_DOSYASI):
            print(f"Hata: {KANAL_DOSYASI} bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        ana_liste_yolu = os.path.join(KLASOR_ADI, ANA_LISTE_ADI)
        
        # SADECE ANA LİSTEYİ AÇIYORUZ
        with open(ana_liste_yolu, "w", encoding="utf-8") as f_main:
            f_main.write("#EXTM3U\n")
            
            for satir in kanallar:
                satir = satir.strip()
                if not satir or ":" not in satir:
                    continue
                
                parca = satir.split(":", 1)
                kanal_adi = parca[0].strip()
                slug = parca[1].strip()
                
                kanal_id = slug.replace("-online", "")
                logo_url = logo_sozlugu.get(kanal_adi, "")
                
                # Link oluştur
                ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                final_link = f"{WORKER_URL}{karakterli_ic_link}"
                
                # ANA LİSTEYE EKLE
                f_main.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                f_main.write(f"{final_link}\n")
                
                print(f"-> {kanal_adi} eklendi.")
        
        print(f"\nİşlem Başarılı! Tek liste oluşturuldu: {ana_liste_yolu}")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
