import re
import os
import urllib.parse
import sys
from curl_cffi import requests

def guncelle():
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    input_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    # Bazı ücretsiz proxy servisleri (GitHub engelini aşmak için aracı)
    # Eğer bunlar çalışmazsa manuel proxy eklemek gerekebilir.
    proxy_listesi = [
        None, # Önce proxiesiz dene
        "http://20.210.113.32:80", # Örnek ücretsiz proxy 1
        "http://172.232.170.181:8080", # Örnek ücretsiz proxy 2
    ]

    print(f"[*] İşlem başlatıldı. Cloudflare aşılmaya çalışılıyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Referer": "https://www.seir-sanduk.com/",
        "Accept-Language": "bg-BG,bg;q=0.9,en-US;q=0.8,tr;q=0.6",
    }

    success = False
    for proxy in proxy_listesi:
        try:
            p_text = "Proxy kullanılıyor" if proxy else "Doğrudan bağlanılıyor"
            print(f"[*] Deneniyor: {p_text}")
            
            response = requests.get(
                GIRIS_URL, 
                impersonate="chrome120", 
                timeout=15,
                headers=headers,
                proxies={"http": proxy, "https": proxy} if proxy else None
            )
            
            if response.status_code == 200:
                success = True
                content = response.text
                break
            else:
                print(f"[-] Hata: {response.status_code}")
        except:
            print("[-] Bağlantı başarısız, sonraki seçenek deneniyor...")

    if not success:
        print("[-] Maalesef tüm erişim yolları kapalı (403). GitHub Actions bu siteye şu an giremiyor.")
        sys.exit(1)

    # Token çekme
    token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + content)
    if not token_match:
        print("[-] Token bulunamadı.")
        sys.exit(1)
        
    token = token_match.group(1)
    print(f"[+] Başarılı! Token: {token}")

    # Kanalları Yazdır
    with open(input_dosyasi, "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
        f_out.write("#EXTM3U\n")
        for satir in satirlar:
            if ":" not in satir: continue
            ad, slug = satir.split(":", 1)
            kanal_id = slug.strip().replace("-online", "")
            player = "12" if "hd" in kanal_id.lower() else "11"
            param_str = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
            link = f"{WORKER_URL}{urllib.parse.quote(param_str, safe='')}"
            f_out.write(f'#EXTINF:-1,{ad.strip()}\n{link}\n')

    print(f"[+] Liste güncellendi: {cikti_dosyasi}")

if __name__ == "__main__":
    guncelle()
