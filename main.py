import cloudscraper
import re

def tum_kanallari_olustur():
    # Şifreni buraya yaz
    sifre = "BURAYA_SIFREYI_YAZ"
    
    url = "https://www.seir-sanduk.com/"
    scraper = cloudscraper.create_scraper()
    
    try:
        print("Kanal listesi çekiliyor...")
        response = scraper.get(url, timeout=30)
        content = response.text
        
        # Sayfadaki tüm kanal linklerini bulur
        # Format genelde şöyledir: id=kanal-adi
        kanal_bulucu = re.findall(r'id=([a-zA-Z0-9_-]+)', content)
        
        # Tekrar eden kanalları temizle
        essiz_kanallar = sorted(list(set(kanal_bulucu)))
        
        m3u_icerik = "#EXTM3U\n"
        
        for kanal_id in essiz_kanallar:
            # Gereksiz veya reklam içerikli id'leri eleyelim
            if len(kanal_id) < 3 or kanal_id in ['player', 'pass', 'submit']:
                continue
                
            kanal_adi = kanal_id.replace('-', ' ').title() # id'yi güzel bir isme dönüştürür
            link = f"https://www.seir-sanduk.com/?player=11&id={kanal_id}&pass={sifre}"
            
            m3u_icerik += f"#EXTINF:-1,{kanal_adi}\n{link}\n"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
            
        print(f"Bitti! Toplam {len(essiz_kanallar)} kanal listeye eklendi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    tum_kanallari_olustur()
