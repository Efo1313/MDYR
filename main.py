import cloudscraper
import re
import time

def guncel_sifreyi_yakala():
    # Sitenin bot korumasını aşmak için en gelişmiş tarayıcı kimliği
    scraper = cloudscraper.create_scraper(
        delay=10, 
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'mobile': False,
        }
    )

    url = "https://www.seir-sanduk.com/"
    
    try:
        # Siteye bağlan ve JS korumasının çözülmesi için bekle
        print("Güvenlik duvarı aşılıyor, lütfen bekleyin...")
        response = scraper.get(url, timeout=45)
        
        # Eğer hala koruma sayfasındaysak içeriği kontrol et
        if "areMouseMovesMostlyStraightLined" in response.text:
            print("HATA: Site hala fare hareketi kontrolü yapıyor.")
            # Alternatif: Mobil tarayıcıyı dene
            scraper = cloudscraper.create_scraper(browser={'browser': 'iphone', 'platform': 'ios'})
            response = scraper.get(url, timeout=45)

        content = response.text
        # Şifre kalıbını ara (Örn: 11kalAd... formatı)
        # Bu sefer daha geniş bir arama yapıyoruz
        match = re.search(r'pass=([a-zA-Z0-9]{25,50})', content)
        
        if match:
            sifre = match.group(1)
            print(f"BAŞARILI! Şifre: {sifre}")
            with open("sifre.txt", "w") as f: f.write(sifre)
            
            # Senin istediğin link formatıyla M3U oluştur
            m3u = f"#EXTM3U\n#EXTINF:-1,bTV HD\nhttps://www.seir-sanduk.com/?player=11&id=hd-btv-hd&pass={sifre}"
            with open("liste.m3u", "w", encoding="utf-8") as f: f.write(m3u)
        else:
            print("Şifre bulunamadı. Site botu tamamen engelledi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncel_sifreyi_yakala()
