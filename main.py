import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # --- AYARLAR ---
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KANAL_DOSYASI = "kanallar.txt"
    LOGO_DOSYASI = "Tv logo.txt"
    CIKTI_DOSYASI = "kanallar.m3u"

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        # 1. Logoları Hafızaya Al
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        p = satir.strip().split(":", 1)
                        logo_sozlugu[p[0].strip()] = p[1].strip()

        # 2. Token Al
        print("Token alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=30)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        if not token_match:
            print("Token bulunamadı!")
            return
        token = token_match.group(1)

        # 3. Kanalları Oku ve Tek Dosyaya Yaz
        if not os.path.exists(KANAL_DOSYASI):
            print("Kanallar.txt bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            
            for satir in kanallar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                kanal_adi, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                player_no = "12" if "hd" in kanal_id.lower() else "11"
                
                # Link Oluşturma
                ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
                final_link = f"{WORKER_URL}{urllib.parse.quote(ic_link, safe='')}"
                
                # Logoyu bul
                logo = logo_sozlugu.get(kanal_adi.strip(), "")
                
                # M3U Formatında Yaz
                f_out.write(f'#EXTINF:-1 tvg-logo="{logo}",{kanal_adi.strip()}\n')
                f_out.write(f"{final_link}\n")

        print(f"BAŞARILI: {CIKTI_DOSYASI} oluşturuldu.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
