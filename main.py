import cloudscraper
import re
import os

def guncelle():
    # 1. Ayarlar
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    
    # Klasör yoksa oluştur
    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)
        print(f"'{KLASOR_ADI}' klasörü oluşturuldu.")

    scraper = cloudscraper.create_scraper()
    
    try:
        # 2. Şifreyi (Token) Al
        print("Siteye giriş yapılıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        token_match = re.search(r'pass=([a-zA-Z0-9]+)', response.url)
        
        if not token_match:
            print("Hata: Şifre (pass) bulunamadı.")
            return
            
        token = token_match.group(1)
        print(f"Güncel Şifre: {token}")

        # 3. Kanalları Oku ve Ayrı Dosyalar Oluştur
        if not os.path.exists("kanallar.txt"):
            print("Hata: kanallar.txt bulunamadı!")
            return

        with open("kanallar.txt", "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        for satir in kanallar:
            if ":" in satir:
                kanal_adi, slug = satir.strip().split(": ")
                
                # Dosya adını temizle (Boşlukları alt tire yap)
                dosya_adi = kanal_adi.replace(" ", "_") + ".m3u"
                dosya_yolu = os.path.join(KLASOR_ADI, dosya_adi)
                
                # Player 11'li link yapısı
                # Not: Eğer Player 11 çalışmazsa aşağıyı {BASE_URL}{slug}?pass={token} yapabilirsin
                final_link = f"{WORKER_URL}{BASE_URL}?player=11&id={slug.replace('-online','')}&pass={token}"
                
                # Sadece linki içeren m3u dosyasını yaz
                with open(dosya_yolu, "w", encoding="utf-8") as f_m3u:
                    f_m3u.write(final_link)
                
                print(f"-> {dosya_adi} oluşturuldu.")
        
        print("\nİşlem Başarılı: Tüm kanallar 'playlist' klasörüne kaydedildi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    guncelle()
