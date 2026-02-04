import cloudscraper
import re
import os
import urllib.parse
import sys

def guncelle():
    # Çalışma dizinini mutlak yol olarak alalım (GitHub Actions için en güvenli yol)
    mevcut_dizin = os.path.dirname(os.path.abspath(__file__))
    
    cikti_dosyasi = os.path.join(mevcut_dizin, "kanallar.m3u")
    input_dosyasi = os.path.join(mevcut_dizin, "kanallar.txt")
    
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"

    # Tarayıcı taklidini güçlendirelim
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        print(f"[*] İşlem başlatıldı. Dizin: {mevcut_dizin}")
        
        # 1. Aşama: Sayfaya erişim ve Token çekme
        response = scraper.get(GIRIS_URL, timeout=30)
        if response.status_code != 200:
            print(f"[-] HATA: Siteye erişilemedi. Durum kodu: {response.status_code}")
            sys.exit(1)

        # Token'ı hem URL'de hem de sayfa içeriğinde arayalım
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url + response.text)
        
        if not token_match:
            print("[-] HATA: Token (pass=...) içeriği bulunamadı! Site koruması değişmiş olabilir.")
            # Sayfa içeriğinin bir kısmını loglara basalım ki ne olduğunu anlayalım
            print(f"Gelen sayfa özeti: {response.text[:200]}...")
            sys.exit(1)
            
        token = token_match.group(1)
        print(f"[+] TOKEN BAŞARIYLA ALINDI: {token}")

        # 2. Aşama: kanallar.txt kontrolü
        if not os.path.exists(input_dosyasi):
            print(f"[-] HATA: {input_dosyasi} dosyası bulunamadı!")
            sys.exit(1)

        with open(input_dosyasi, "r", encoding="utf-8") as f:
            satirlar = f.readlines()

        # 3. Aşama: m3u dosyasını oluşturma
        kanal_sayisi = 0
        with open(cikti_dosyasi, "w", encoding="utf-8") as f_out:
            f_out.write("#EXTM3U\n")
            for satir in satirlar:
                satir = satir.strip()
                if not satir or ":" not in satir:
                    continue
                
                ad, slug = satir.split(":", 1)
                kanal_id = slug.strip().replace("-online", "")
                
                # HD kontrolü ile player seçimi
                player = "12" if "hd" in kanal_id.lower() else "11"
                
                # Link oluşturma (Worker URL yapısına uygun)
                parametreler = f"{BASE_URL}?player={player}&id={kanal_id}&pass={token}"
                encoded_param = urllib.parse.quote(parametreler, safe='')
                link = f"{WORKER_URL}{encoded_param}"
                
                f_out.write(f"#EXTINF:-1,{ad.strip()}\n{link}\n")
                kanal_sayisi += 1

        print(f"[+] İŞLEM TAMAMLANDI!")
        print(f"[+] {kanal_sayisi} kanal başarıyla işlendi.")
        print(f"[+] Dosya yolu: {cikti_dosyasi}")
        print(f"[+] Dosya boyutu: {os.path.getsize(cikti_dosyasi)} byte")

    except Exception as e:
        print(f"[!] BEKLENMEDİK HATA: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    guncelle()
