import cloudscraper
import re
import os

def generate_m3u():
    # 1. Cloudflare korumasını aşmak için scraper oluştur
    scraper = cloudscraper.create_scraper()
    
    # Giriş linki
    login_url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    
    try:
        # 2. Siteye git ve yönlendirildiği güncel adresi al
        response = scraper.get(login_url, timeout=15)
        current_url = response.url
        print(f"Giris yapildi: {current_url}")
        
        # 3. URL içindeki 'pass=' değerini ayıkla
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', current_url)
        if not token_match:
            print("Hata: Token (pass) bulunamadi!")
            return
        
        token = token_match.group(1)
        
        # 4. kanallar.txt dosyasını oku ve m3u oluştur
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt dosyasi bulunamadi!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open("liste.m3u", "w", encoding="utf-8") as m3u:
            m3u.write("#EXTM3U\n")
            for line in lines:
                if ":" in line:
                    name, slug = line.strip().split(": ")
                    # M3U formatında yaz
                    m3u.write(f"#EXTINF:-1,{name}\n")
                    m3u.write(f"https://www.seir-sanduk.com/{slug}?pass={token}\n")
        
        print("liste.m3u başarıyla güncellendi.")

    except Exception as e:
        print(f"Bir hata olustu: {e}")

if __name__ == "__main__":
    generate_m3u()
