import urllib.request
import os

def guncel_sifre_al():
    """Seir-Sanduk sitesinden güncel pass anahtarını çeker."""
    try:
        url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            sifre = response.read().decode('utf-8').strip()
            print(f"Sifre alindi: {sifre}")
            return sifre
    except Exception as e:
        print(f"Sifre alma hatasi: {e}")
        return None

def liste_olustur():
    sifre = guncel_sifre_al()
    if not sifre:
        return

    m3u_icerik = "#EXTM3U\n"
    dosya_bulundu = False

    # kanallar.txt dosyasini okuyoruz
    try:
        # GitHub Actions ortaminda dosya yolunu garantiye aliyoruz
        base_path = os.path.dirname(__file__)
        txt_path = os.path.join(base_path, "kanallar.txt")
        
        with open(txt_path, "r", encoding="utf-8") as f:
            for satir in f:
                satir = satir.strip()
                if satir and ":" in satir:
                    # 'Kanal Adi: kanal-id' formatini ayiriyoruz
                    ad, id_kod = satir.split(":", 1)
                    ad = ad.strip()
                    id_kod = id_kod.strip()
                    
                    # Workers linkini olusturuyoruz
                    link = f"http://tv.seirsanduk.workers.dev/?ID=https://www.seir-sanduk.com/{id_kod}?pass={sifre}"
                    m3u_icerik += f"#EXTINF:-1,{ad}\n{link}\n"
                    dosya_bulundu = True
    except FileNotFoundError:
        print("HATA: kanallar.txt dosyasi bulunamadi! Lutfen bu dosyayi olusturun.")
        return

    if dosya_bulundu:
        # Nihai M3U dosyasini kaydediyoruz
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
        print("liste.m3u basariyla guncellendi.")
    else:
        print("HATA: kanallar.txt ici bos veya hatali formatta.")

if __name__ == "__main__":
    liste_olustur()
