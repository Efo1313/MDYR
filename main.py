import cloudscraper
import re
import os
import urllib.parse
import sys
import time

def guncelle():
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    input_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    # 403 hatasını aşmak için geliştirilmiş tarayıcı ayarları
    scraper = cloudscraper.create_scraper(
        delay=10, 
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True,
            'mobile': False
        }
    )
    
    # Gerçekçi HTTP Header'ları ekleyelim
    scraper.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    })

    try:
        print(f"[*] İşlem başlatıldı. Hedef: {GIRIS_URL}")
        
        # Cloudflare'in çözülmesi için bazen kısa bir bekleme gerekir
        time.sleep(2) 
        
        response = scraper.get(GIRIS_URL, timeout=30)
        
        if response.status_code == 403:
            print("[-] HATA: 403 Forbidden (Cloudflare engeli).")
            # Alternatif yöntem: Normal request deneyelim
            print("[*] Alternatif yöntem deneniyor...")
            response = scraper.get(GIRIS_URL, allow_redirects=True)

        if response.status_code != 200:
            print(f"[-] HATA: Siteye hala erişilemiyor. Kod: {response.status_code}")
            sys.exit(1)

        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        
        if not token_match:
            print("[-] HATA: Sayfa açıldı ama Token bulunamadı!")
            sys.exit(1)
            
        token = token_match.group(1)
        print(f"[+] TOKEN ALINDI: {token}")

        if not os.path.exists(input_dosyasi):
            print(f"[-] HATA: {input_dosyasi} bulunamadı!")
            sys.exit(1)

        with open(input_dosyasi, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            kanal_sayisi = 0
            for satir in satirlar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                ad, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                parametreler = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                encoded_param = urllib.parse.quote(parametreler, safe='')
                link = f"{WORKER_URL}{encoded_param}"
                
                f_out.write(f"#EXTINF:-1,{ad.strip()}\n{link}\n")
                kanal_sayisi += 1

        print(f"[+] BAŞARILI: {kanal_sayisi} kanal kaydedildi.")

    except Exception as e:
        print(f"[!] HATA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    guncelle()
