import re
import os
import urllib.parse
import sys
from curl_cffi import requests

def guncelle():
    # Dosya yolları
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    logo_dosyasi = os.path.join(mevcut_dizin, "TV logosu.txt")
    kanal_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    print("[*] Logolar yükleniyor...")
    logolar = {}
    if os.path.exists(logo_dosyasi):
        with open(logo_dosyasi, "r", encoding="utf-8") as f:
            for satir in f:
                if ":" in satir:
                    ad, logo = satir.split(":", 1)
                    logolar[ad.strip().lower()] = logo.strip()
    
    print("[*] Siteye bağlanılıyor (Token alınıyor)...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Referer": "https://www.seir-sanduk.com/"
    }

    try:
        # Pydroid'de çalıştırırken 403 almazsın
        response = requests.get(GIRIS_URL, impersonate="chrome120", headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"[-] Hata: Siteye girilemedi. Kod: {response.status_code}")
            return

        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        if not token_match:
            print("[-] Hata: Token bulunamadı.")
            return
            
        token = token_match.group(1)
        print(f"[+] Bağlantı Başarılı! Token: {token}")

        if not os.path.exists(kanal_dosyasi):
            print(f"[-] Hata: {kanal_dosyasi} bulunamadı!")
            return

        with open(kanal_dosyasi, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            for satir in kanallar:
                if ":" not in satir: continue
                ad_orj, slug = satir.split(":", 1)
                ad = ad_orj.strip()
                kanal_id = slug.strip().replace("-online", "")
                
                # Logoyu bul (küçük harfe çevirerek eşleştir)
                logo_linki = logolar.get(ad.lower(), "")
                
                player = "12" if "hd" in kanal_id.lower() else "11"
                param_str = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                link = f"{WORKER_URL}{urllib.parse.quote(param_str, safe='')}"
                
                f_out.write(f'#EXTINF:-1 tvg-logo="{logo_linki}",{ad}\n{link}\n')

        print(f"[+] BİTTİ! {cikti_dosyasi} dosyası başarıyla oluşturuldu.")

    except Exception as e:
        print(f"[!] Hata: {str(e)}")

if __name__ == "__main__":
    guncelle()
