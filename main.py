import cloudscraper
import re
import os
import urllib.parse

def guncelle():
    # --- AYARLAR ---
    GIRIS_URL = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
    WORKER_URL = "https://tv.seirsanduk.workers.dev/?ID="
    BASE_URL = "https://www.seir-sanduk.com/"
    KLASOR_ADI = "playlist"
    KANAL_DOSYASI = "kanallar.txt"
    LOGO_DOSYASI = "Tv logo.txt"
    ANA_LISTE_ADI = "TUM_KANALLAR.m3u"

    if not os.path.exists(KLASOR_ADI):
        os.makedirs(KLASOR_ADI)

    # Bot engellerini aşmak için tarayıcı gibi davranıyoruz
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        # 1. Logoları oku
        logo_sozlugu = {}
        if os.path.exists(LOGO_DOSYASI):
            with open(LOGO_DOSYASI, "r", encoding="utf-8") as f:
                for satir in f:
                    if ":" in satir:
                        p = satir.strip().split(":", 1)
                        logo_sozlugu[p[0].strip()] = p[1].strip()

        # 2. Güncel Token'ı (pass) Al
        print("Siteden güncel anahtar (token) alınıyor...")
        response = scraper.get(GIRIS_URL, timeout=20)
        
        # Token Yakalama Mantığı (Geliştirildi)
        token = None
        
        # Önce yönlendirilen URL'de "pass=" ara
        token_match = re.search(r'pass=([^&"\'\s>]+)', response.url)
        
        if not token_match:
            # URL'de yoksa sayfa içeriğinde ara
            token_match = re.search(r'pass=([^&"\'\s>]+)', response.text)

        if token_match:
            token = token_match.group(1)
            # Eğer token başında gereksiz karakterler (örneğin player id) kalırsa temizle
            # Genelde pass kodu uzun bir harf/sayı dizisidir
            print(f"Token bulundu: {token}")
        else:
            print("HATA: Token bulunamadı! Site koruması aktif olabilir.")
            return

        # 3. Kanalları oku
        if not os.path.exists(KANAL_DOSYASI):
            print(f"HATA: {KANAL_DOSYASI} bulunamadı!")
            return

        with open(KANAL_DOSYASI, "r", encoding="utf-8") as f:
            kanallar = f.readlines()

        # --- ANA LİSTE OLUŞTURMA ---
        ana_liste_yolu = os.path.join(KLASOR_ADI, ANA_LISTE_ADI)
        with open(ana_liste_yolu, "w", encoding="utf-8") as f_ana:
            f_ana.write("#EXTM3U\n")

            for satir in kanallar:
                satir = satir.strip()
                if not satir or ":" not in satir: continue
                
                parca = satir.split(":")
                kanal_adi = parca[0].strip()
                kanal_id = parca[1].strip().replace("-online", "")
                
                # Eğer kanallar.txt içinde player belirtilmemişse 11 kullan
                player_no = parca[2].strip() if len(parca) > 2 else "11"
                
                # Linki Oluştur
                ic_link = f"{BASE_URL}?player={player_no}&id={kanal_id}&pass={token}"
                
                # Worker uyumlu URL encoding (safe parametresi boş bırakıldı)
                encoded_link = urllib.parse.quote(ic_link, safe='')
                final_link = f"{WORKER_URL}{encoded_link}"
                
                # A) TUM_KANALLAR.m3u Yazımı
                logo_url = logo_sozlugu.get(kanal_adi, "")
                f_ana.write(f'#EXTINF:-1 tvg-logo="{logo_url}",{kanal_adi}\n')
                f_ana.write(f"{final_link}\n")

                # B) Tekil Dosyalar
                temiz_ad = "".join([c for c in kanal_adi if c.isalnum() or c in (' ', '_')]).rstrip()
                tekil_dosya_yolu = os.path.join(KLASOR_ADI, f"{temiz_ad}.m3u8")
                
                with open(tekil_dosya_yolu, "w", encoding="utf-8") as f_tekil:
                    f_tekil.write(final_link)

            print(f"\nİşlem Başarılı! {len(kanallar)} kanal güncellendi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    guncelle()
