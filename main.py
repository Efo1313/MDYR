import requests
import re
from bs4 import BeautifulSoup

def guncel_sifreyi_yakala():
    url = "https://www.seir-sanduk.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # 1. Yöntem: Sayfa içindeki tüm href linklerini tara
        # Senin paylaştığın şifre gibi uzun (30+ karakter) olanları bul
        pass_matches = re.findall(r'pass=([a-zA-Z0-9]{30,})', response.text)
        
        if not pass_matches:
            # 2. Yöntem: Script bloklarının içindeki tırnaklı uzun dizeleri tara
            pass_matches = re.findall(r'["\']([a-zA-Z0-9]{30,})["\']', response.text)

        if pass_matches:
            # En son/en güncel görünen şifreyi al
            yeni_sifre = pass_matches[0]
            print(f"BAŞARILI! Güncel Şifre Bulundu: {yeni_sifre}")

            # Dosyaya kaydet
            with open("sifre.txt", "w") as f:
                f.write(yeni_sifre)
            
            # Senin paylaştığın formata uygun M3U kanal linki oluştur
            # Örnek: bTV HD kanalı için
            m3u_icerik = f"#EXTM3U\n"
            m3u_icerik += f"#EXTINF:-1,bTV HD\nhttps://www.seir-sanduk.com/?player=11&id=hd-btv-hd&pass={yeni_sifre}\n"
            
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_icerik)
                
            print("sifre.txt ve liste.m3u başarıyla güncellendi.")
        else:
            print("HATA: Sayfada senin verdiğin formata uygun uzun bir şifre bulunamadı.")
            # Hata tespiti için sayfanın bir kısmını yazdıralım
            print("Sayfa başlığı:", response.text[:200])

    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    guncel_sifreyi_yakala()
