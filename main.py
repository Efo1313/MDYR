import cloudscraper
import os
import re
from urllib.parse import quote

def verileri_yakala():
    try:
        # Tarayıcıyı birebir taklit ediyoruz
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
        
        # 1. Adım: Senin tıkladığın o ana linke gidip oturum açıyoruz
        ana_url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        response = scraper.get(ana_url, timeout=15)
        
        # 2. Adım: Adres çubuğunda gördüğün o pass şifresini ayıklıyoruz
        # Önce URL içinden bakıyoruz, yoksa sayfa içeriğinden
        sifre = None
        # Sayfa içeriğinden en az 30 karakterlik karmaşık şifreyi bul
        match = re.search(r'[a-zA-Z0-9]{30,}', response.text)
        if match:
            sifre = match.group(0)
            print(f"Oturum Anahtari Yakalandi: {sifre}")
            return sifre
        
        return None
    except Exception as e:
        print(f"Oturum acma hatasi: {e}")
        return None

def liste_olustur():
    sifre = verileri_yakala()
    if not sifre:
        print("Sifre alinamadi, siteye ulasilamiyor olabilir.")
        return

    m3u_icerik = "#EXTM3U\n"
    try:
        with open("kanallar.txt", "r", encoding="utf-8") as f:
            for satir in f:
                if ":" in satir:
                    ad, id_kod = satir.split(":", 1)
                    # ID'yi temizle (hd-bnt-1-hd-online -> hd-bnt-1-hd)
                    temiz_id = id_kod.strip().replace("-online", "")
                    
                    # Sitenin kanal acarken kullandigi orijinal yapi
                    # id parametresinden sonra pass parametresini ekliyoruz
                    hedef_url = f"https://www.seir-sanduk.com/?player=11&id={temiz_id}&pass={sifre}"
                    
                    # Workers Linki (Encoding yapılmış)
                    encoded_url = quote(hedef_url, safe='')
                    m3u_icerik += f"#EXTINF:-1,{ad.strip()}\nhttp://tv.seirsanduk.workers.dev/?ID={encoded_url}\n"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print("Liste.m3u en taze oturum bilgisiyle güncellendi.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    liste_olustur()
