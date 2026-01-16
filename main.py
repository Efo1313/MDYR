import cloudscraper
import re
import os

def guncel_sifreyi_al():
    # Cloudflare engellerini aşmak için scraper oluşturur
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    url = "https://www.seir-sanduk.com/"
    
    print("Siteye bağlanılıyor (Bot koruması aşılıyor)...")

    try:
        # Site içeriğini çek
        response = scraper.get(url, timeout=30)
        content = response.text
        
        # Senin paylaştığın uzun şifre formatını (30+ karakter) ara
        # Örn: 11kalAdKaAde11sF8F01011616011601
        match = re.search(r'pass=([a-zA-Z0-9]{30,})', content)
        
        if match:
            yeni_sifre = match.group(1)
            print(f"BAŞARILI! Bulunan Şifre: {yeni_sifre}")
            
            # Şifreyi dosyaya kaydet
            with open("sifre.txt", "w") as f:
                f.write(yeni_sifre)
            
            # Kanal listesini (M3U) oluştur
            m3u_icerik = f"#EXTM3U\n#EXTINF:-1,Seir Sanduk TV\nhttps://www.seir-sanduk.com/live.php?id=hd-btv-hd&pass={yeni_sifre}"
            with open("liste.m3u", "w", encoding="utf-8") as f:
                f.write(m3u_icerik)
                
            print("Dosyalar güncellendi.")
        else:
            print("HATA: Şifre bulunamadı. Site yapısı değişmiş veya koruma aşılamadı.")
            # Hata analizi için sayfa başlığını yazdır
            print("Sayfa içeriği özeti:", content[:300])

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    guncel_sifreyi_al()
