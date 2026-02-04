import re
import os
import urllib.parse
import sys
from curl_cffi import requests

def guncelle():
    # Dizin ayarları
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    input_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    
    # Seir-Sanduk URL yapıları
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    try:
        print(f"[*] İşlem başlatıldı. Cloudflare aşılıyor...")
        
        # Ekstra başlıklar ekleyerek bot korumasını daha iyi kandıralım
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.seir-sanduk.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,bg;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"
        }
        
        # impersonate="chrome120" Cloudflare aşmak için en iyisidir
        response = requests.get(
            GIRIS_URL, 
            impersonate="chrome120", 
            timeout=30,
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"[-] HATA: Siteye erişilemedi. Durum Kodu: {response.status_code}")
            # Hata 403 ise detay verelim
            if response.status_code == 403:
                print("[!] Cloudflare IP adresini engellemiş (GitHub Actions IP'si yasaklı olabilir).")
            sys.exit(1)

        content = response.text
        # Token arama mantığını güçlendirelim
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + content)
        
        if not token_match:
            print("[-] HATA: Token bulunamadı. Sayfa içeriği değişmiş veya yanlış yere bakıyoruz.")
            # Hata ayıklama için sayfanın bir kısmını yazdıralım
            print(f"[*] Gelen içerik özeti: {content[:200]}")
            sys.exit(1)
            
        token = token_match.group(1)
        print(f"[+] BAĞLANTI BAŞARILI! Token Alındı: {token}")

        if not os.path.exists(input_dosyasi):
            print(f"[-] HATA: Giriş dosyası ({input_dosyasi}) bulunamadı!")
            sys.exit(1)

        with open(input_dosyasi, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        kanal_sayisi = 0
        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            for satir in satirlar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                ad, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                
                # HD kontrolü ve Player seçimi
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                param_str = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                encoded_param = urllib.parse.quote(param_str, safe='')
                link = f"{WORKER_URL}{encoded_param}"
                
                f_out.write(f'#EXTINF:-1 tvg-name="{ad.strip()}",{ad.strip()}\n{link}\n')
                kanal_sayisi += 1

        print(f"[+] BAŞARILI: {kanal_sayisi} kanal '{cikti_dosyasi}' dosyasına kaydedildi.")

    except Exception as e:
        print(f"[!] BEKLENMEDİK KRİTİK HATA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    guncelle()
