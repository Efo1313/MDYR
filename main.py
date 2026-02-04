import re
import os
import urllib.parse
import sys
import time
from curl_cffi import requests

def guncelle():
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    input_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    
    # Seir-Sanduk URL Yapıları
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    print("[*] Bağlantı girişimi başlatılıyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "bg-BG,bg;q=0.9,en-US;q=0.8,tr;q=0.6",
        "Referer": "https://www.seir-sanduk.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # GitHub engeline karşı 3 deneme yapalım
        response = None
        for i in range(3):
            print(f"[*] Deneme {i+1}/3...")
            try:
                response = requests.get(
                    GIRIS_URL, 
                    impersonate="chrome120", 
                    headers=headers, 
                    timeout=20
                )
                if response.status_code == 200: break
            except Exception as e:
                print(f"[-] Deneme başarısız: {e}")
                time.sleep(2)

        if not response or response.status_code != 200:
            print(f"[-] KRİTİK HATA: Site hala 403 veriyor. GitHub IP'si tamamen bloklanmış.")
            print("[!] ÇÖZÜM: Bu işlemi telefonda Pydroid 3 uygulamasıyla yapmalısın.")
            sys.exit(1)

        content = response.text
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + content)
        
        if not token_match:
            print("[-] HATA: Token bulunamadı.")
            sys.exit(1)
            
        token = token_match.group(1)
        print(f"[+] Token Başarıyla Alındı: {token}")

        # Kanallar.txt dosyasını kontrol et
        if not os.path.exists(input_dosyasi):
            print(f"[-] HATA: {input_dosyasi} bulunamadı!")
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
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                param_str = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                encoded_param = urllib.parse.quote(param_str, safe='')
                link = f"{WORKER_URL}{encoded_param}"
                
                f_out.write(f'#EXTINF:-1 tvg-logo="",{ad.strip()}\n{link}\n')
                kanal_sayisi += 1

        print(f"[+] İŞLEM TAMAM! {kanal_sayisi} kanal güncellendi.")

    except Exception as e:
        print(f"[!] BEKLENMEDİK HATA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    guncelle()
