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

    # Klasör yoksa oluştur
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    scraper = cloudscraper.create_scraper()
    
    try:
        # 1. LOGOLARI SÖZLÜĞE AL
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        parca = satir.strip().split(":", 1)
                        logo_sozlugu[parca[0].strip()] = parca[1].strip()

        # 2. GÜNCEL PASS TOKEN'I AL
        print("Token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        if not token_match:
            print("Hata: Token bulunamadı!")
            return
        token = token_match.group(1)

        # 3. KANALLARI OKU VE AYRI DOSYALAR OLUŞTUR
        if not os.path.exists(KANAL_DOSYASI):
            print(f"Hata: {KANAL_DOSYASI} bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            satir = satir.strip()
            if not satir or ":" not in satir:
                continue
            
            parca = satir.split(":", 1)
            kanal_adi = parca[0].strip()
            slug = parca[1].strip()
            
            kanal_id = slug.replace("-online", "")
            logo_url = logo_sozlugu.get(kanal_adi, "")
            
            # --- YÜZDELİ KARAKTERLERİ OLUŞTURUYORUZ ---
            ic_link = f"{BASE_URL}?player=11&id={kanal_id}&pass={token}"
            karakterli_ic_link = urllib.parse.quote(ic_link, safe='')
            final_link = f"{WORKER_URL}{karakterli_ic_link}"
            
            # Dosya adını temizle (Sistemde sorun çıkmaması için)
            dosya_adi = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
            dosya_yolu = os.path.join(KLASOR_ADI, f"{dosya_adi}.m3u")
            
            # --- TEKİL DOSYAYI YAZ ---
            with open(dosya_yolu, "w", encoding="utf-8") as f_out:
                f_out.write("#EXTM3U\n")
                f_out.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                f_out.write(f"{final_link}\n")
            
            print(f"Oluşturuldu: {dosya_adi}.m3u")

        print(f"\nİşlem Başarılı! Kanallar yüzdelikli karakterlerle '{KLASOR_ADI}' klasörüne tek tek kaydedildi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
