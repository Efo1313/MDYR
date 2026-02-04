import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # Dosyanın tam yolunu bulalım ki "nereye yazdı" derdi bitsin
    mevcut_dizin = os.getcwd()
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','desktop': True})
    
    try:
        print(f"Çalışma dizini: {mevcut_dizin}")
        response = scraper.get(GIRIS_URL, timeout=30)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        
        if not token_match:
            print("HATA: Token bulunamadı!")
            return
            
        token = token_match.group(1)
        print(f"TOKEN ALINDI: {token}")

        # kanallar.txt dosyasını oku
        if not os.path.exists("kanallar.txt"):
            print("HATA: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            for satir in satirlar:
                satir = satir.strip()
                if ":" not in satir: continue
                
                ad, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                link = f"{WORKER_URL}{urllib.parse.quote(f'{BASE_URL}?player={player}&id={kanal_id}&pass={token}', safe='')}"
                f_out.write(f"#EXTINF:-1,{ad.strip()}\n{link}\n")

        print(f"DOSYA YAZILDI: {cikti_dosyasi}")
        print(f"Dosya boyutu: {os.path.getsize(cikti_dosyasi)} byte")

    except Exception as e:
        print(f"Sistemsel Hata: {e}")

if __name__ == "__main__":
    guncelle()
