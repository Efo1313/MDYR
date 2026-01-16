import cloudscraper
import os
import re
from urllib.parse import quote

def guncel_sifre_al():
    try:
        scraper = cloudscraper.create_scraper()
        # Senin verdiğin parola linki
        url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        response = scraper.get(url).text
        
        # HTML etiketlerini temizle ve sadece şifre olan kısmı al
        sifre = re.sub('<[^<]+?>', '', response).strip()
        
        # Eğer site hata verip tüm sayfayı dönerse, içinden şifreye benzeyen bloğu seç
        if len(sifre) > 100:
            match = re.search(r'[A-Za-z0-9]{20,}', sifre)
            if match:
                sifre = match.group(0)
        
        return sifre
    except:
        return None

def liste_olustur():
    sifre = guncel_sifre_al()
    if not sifre:
        print("Sifre alinamadi!")
        return

    m3u_icerik = "#EXTM3U\n"
    
    try:
        with open("kanallar.txt", "r", encoding="utf-8") as f:
            for satir in f:
                if ":" in satir:
                    ad, id_kod = satir.split(":", 1)
                    ad = ad.strip()
                    # Örn: bnt-1-hd-online -> bnt-1-hd
                    temiz_id = id_kod.strip().replace("-online", "")
                    if temiz_id.startswith("hd-"):
                        temiz_id = temiz_id # Zaten hd- ile başlıyor
                    
                    # SENİN İSTEDİĞİN ÖRNEK FORMAT:
                    # ?player=11&id=kanal-id&pass=sifre
                    hedef_link = f"https://www.seir-sanduk.com/?player=11&id={temiz_id}&pass={sifre}"
                    
                    # Workers linki ve URL Encoding (Gerekli karakter dönüşümü)
                    encoded_link = quote(hedef_link, safe='')
                    final_link = f"http://tv.seirsanduk.workers.dev/?ID={encoded_link}"
                    
                    m3u_icerik += f"#EXTINF:-1,{ad}\n{final_link}\n"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print(f"Liste olusturuldu! Kullanilan Sifre: {sifre}")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    liste_olustur()
