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
    
    # DOSYA İSİMLERİ (Senin verdiğin isimler)
    KANAL_DOSYASI = "kanallar.txt"
    LOGO_DOSYASI = "Tv logo.txt"

    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 1. LOGO LİNKERİNİ HAFIZAYA AL
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        # "BNT 1 HD : https://..." şeklinde ayırır
                        k_adi, l_link = satir.strip().split(" : ", 1)
                        logo_sozlugu[k_adi.strip()] = l_link.strip()
        else:
            print(f"Hata: {LOGO_DOSYASI} bulunamadı!")
            return

        # 2. GÜNCEL TOKEN AL
        print("Siteden güncel token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Token bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"Başarılı! Token: {token}")

        # 3. KANALLARI OKU VE M3U OLUŞTUR
        if not os.path.exists(KANAL_DOSYASI):
            print(f"Hata: {KANAL_DOSYASI} bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        ana_liste_yolu = os.path.join(KLASOR_ADI, ANA_LISTE_ADI)
        
        with open(ana_liste_yolu, "w", encoding="utf-8") as f_main:
            f_main.write("#EXTM3U\n")
            
            for satir in kanallar:
                if ":" in satir:
                    kanal_adi, slug = satir.strip().split(": ")
                    kanal_id = slug.replace("-online", "")
                    
                    # LOGOYU TV LOGO.TXT DOSYASINDAN ÇEK
                    # Eğer listede yoksa boş bırakır
                    logo_url = logo_sozlugu.get(kanal_adi.strip(), "")
                    
                    # KARAKTERLİ LİNK (URL ENCODING)
                    ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                    karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
                    
                    # FİNAL LİNK
                    final_link = f"{WORKER_URL}{karakterli_ic_link}"
                    
                    # M3U DOSYASINA YAZ
                    f_main.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                    f_main.write(f"{final_link}\n")
                    
                    print(f"-> {kanal_adi} eklendi.")
        
        print(f"\nİşlem Başarılı! Liste oluşturuldu: {ana_liste_yolu}")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    guncelle()
