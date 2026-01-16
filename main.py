import cloudscraper
import os
import re

def guncel_sifre_al():
    try:
        # Web sitesinin korumasını geçmek için scraper kullanıyoruz
        scraper = cloudscraper.create_scraper()
        url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        response = scraper.get(url).text
        
        # HTML kodlarının arasından SADECE şifreyi (harf ve rakamları) çekiyoruz
        # Şifre genellikle kısa bir metindir, HTML taglarını temizliyoruz
        sifre = re.sub('<[^<]+?>', '', response).strip()
        
        # Eğer hala çok uzunsa (HTML gelmişse), ilk kelimeyi almayı dene
        if len(sifre) > 50: 
            sifre = sifre.split()[0]
            
        print(f"Temizlenmis Sifre: {sifre}")
        return sifre
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

def liste_olustur():
    sifre = guncel_sifre_al()
    if not sifre: return

    m3u_icerik = "#EXTM3U\n"
    try:
        with open("kanallar.txt", "r", encoding="utf-8") as f:
            for satir in f:
                if ":" in satir:
                    ad, id_kod = satir.split(":", 1)
                    link = f"http://tv.seirsanduk.workers.dev/?ID=https://www.seir-sanduk.com/{id_kod.strip()}?pass={sifre}"
                    m3u_icerik += f"#EXTINF:-1,{ad.strip()}\n{link}\n"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print("Liste tertemiz bir sekilde olusturuldu!")
    except Exception as e:
        print(f"Liste yazma hatasi: {e}")

if __name__ == "__main__":
    liste_olustur()
