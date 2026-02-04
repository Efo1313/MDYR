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
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    try:
        print(f"[*] İşlem başlatıldı. Cloudflare aşılıyor...")
        
        # curl_cffi ile Chrome 120 parmak izi taklidi
        response = requests.get(
            GIRIS_URL, 
            impersonate="chrome120", 
            timeout=30,
            headers={
                "Referer": "https://www.google.com/",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8"
            }
        )
        
        if response.status_code != 200:
            print(f"[-] HATA: Siteye erişilemedi. Kod: {response.status_code}")
            sys.exit(1)

        # Token çekme (URL ve Text içinde arama)
        content = response.text
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + content)
        
        if not token_match:
            print("[-] HATA: Token bulunamadı. Sayfa yapısı değişmiş olabilir.")
            sys.exit(1)
            
        token = token_match.group(1)
        print(f"[+] BAĞLANTI BAŞARILI! Token: {token}")

        # Kanallar.txt okuma
        if not os.path.exists(input_dosyasi):
            print(f"[-] HATA: {input_dosyasi} dosyası bulunamadı!")
            sys.exit(1)

        with open(input_dosyasi, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        # Yazma işlemi
        kanal_sayisi = 0
        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            for satir in satirlar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                ad, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                param_str = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                encoded_param = urllib.parse.quote(param_str, safe='')
                link = f"{WORKER_URL}{encoded_param}"
                
                f_out.write(f"#EXTINF:-1,{ad.strip()}\n{link}\n")
                kanal_sayisi += 1

        print(f"[+] İŞLEM TAMAM: {kanal_sayisi} kanal m3u dosyasına yazıldı.")

    except Exception as e:
        print(f"[!] BEKLENMEDİK KRİTİK HATA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    guncelle()
