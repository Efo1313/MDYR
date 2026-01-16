import cloudscraper
import re

def guncel_liste_olustur():
    # Şifreyi üreten gizli adres
    sifre_kaynagi = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    scraper = cloudscraper.create_scraper()

    try:
        # 1. Şifreyi çek
        response = scraper.get(sifre_kaynagi)
        # Linkin içinden pass= kısmından sonrasını yakala
        match = re.search(r'pass=([a-zA-Z0-9]+)', response.text)
        
        if match:
            sifre = match.group(1)
            print(f"Yeni Şifre Bulundu: {sifre}")

            # 2. Kanal listesini hazırla
            kanal_idleri = [
                "hd-btv-hd", "btv-action-hd", "btv-cinema-hd", "btv-comedy-hd", "btv-story-hd", "ring-hd",
                "nova-tv-hd", "diema-hd", "diema-family-hd", "kinonova-hd", "nova-sport-hd",
                "diema-sport-hd", "diema-sport-2-hd", "diema-sport-3-hd", "max-sport-1-hd", 
                "max-sport-2-hd", "max-sport-3-hd", "max-sport-4-hd", "bnt-1-hd", "bnt-2-hd", "hbo-hd-bg"
            ]

            m3u_icerik = "#EXTM3U\n"
            for kid in kanal_idleri:
                ad = kid.replace("-", " ").upper()
                link = f"https://www.seir-sanduk.com/?player=11&id={kid}&pass={sifre}"
                m3u_icerik += f"#EXTINF:-1,{ad}\n{link}\n"

            # 3. Kaydet
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_icerik)
            print("Liste.m3u başarıyla güncellendi!")
        else:
            print("Şifre sayfada bulunamadı.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncel_liste_olustur()
