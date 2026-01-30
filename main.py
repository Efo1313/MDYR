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
    KANAL_DOSYASI = "kanallar.txt"
    LOGO_DOSYASI = "Tv logo.txt"
    ANA_LISTE_ADI = "TUM_KANALLAR.m3u"

    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 1. LOGOLARI VE KANALLARI HAZIRLA
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        p = satir.strip().split(":", 1)
                        logo_sozlugu[p[0].strip()] = p[1].strip()

        # 2. GÜNCEL TOKEN'I AL
        print("Token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        if not token_match: return
        token = token_match.group(1)

        # 3. KANALLARI OKU
        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        # --- ANA LİSTE (TUM_KANALLAR.m3u) İÇİN HAZIRLIK ---
        ana_liste_yolu = os.path.join(KLASOR_ADI, ANA_LISTE_ADI)
        with open(ana_liste_yolu, "w", encoding="utf-8") as f_ana:
            f_ana.write("#EXTM3U\n")

            for satir in kanallar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                parca = satir.split(":", 1)
                kanal_adi = parca[0].strip()
                slug = parca[1].strip()
                kanal_id = slug.replace("-online", "")
                
                # Link Oluşturma (Yüzdelikli)
                ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
                encoded_link = urllib.parse.quote(ic_link, safe='')
                final_link = f"{WORKER_URL}{encoded_link}"
                
                # A) ANA LİSTEYE EKLE (ESKİ FORMAT: LOGO VE İSİMLE)
                logo_url = logo_sozlugu.get(kanal_adi, "")
                f_ana.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                f_ana.write(f"{final_link}\n")

                # B) TEKİL DOSYAYI OLUŞTUR (YENİ FORMAT: SADECE SAF ADRES)
                temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
                tekil_dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u")
                
                with open(tekil_dosya_yolu, "w", encoding="utf-8") as f_tekil:
                    f_tekil.write(final_link) # SADECE LİNK

            print(f"İşlem tamamlandı.")
            print(f"- {ANA_LISTE_ADI} (Formatlı ana liste güncellendi)")
            print(f"- Diğer tüm kanallar (Saf adres olarak tek tek oluşturuldu)")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
