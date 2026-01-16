import os

def liste_hazirla():
    # FORUMDAN ALDIĞIN ŞİFREYİ AŞAĞIYA YAPIŞTIR
    sifre = "11kalAdKaAde11sF8F01011616011601" 

    # Seir-Sanduk üzerindeki popüler kanal ID'leri
    kanal_idleri = [
        "hd-btv-hd", "nova-tv-hd", "diema-sport-hd", "diema-sport-2-hd",
        "diema-sport-3-hd", "max-sport-1-hd", "max-sport-2-hd", "max-sport-3-hd",
        "max-sport-4-hd", "hbo-hd-bg", "hbo-2-hd-bg", "hbo-3-hd-bg",
        "bnt-1-hd", "bnt-2-hd", "bnt-3-hd", "btv-action-hd", "btv-cinema-hd",
        "btv-comedy-hd", "btv-story-hd", "ring-hd", "diema-family-hd", "kinonova-hd"
    ]

    m3u_icerik = "#EXTM3U\n"
    
    for kid in kanal_idleri:
        adi = kid.replace("-", " ").upper()
        link = f"https://www.seir-sanduk.com/?player=11&id={kid}&pass={sifre}"
        m3u_icerik += f"#EXTINF:-1,{adi}\n{link}\n"

    # Dosyaları oluştur
    with open("liste.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    with open("sifre.txt", "w") as f:
        f.write(sifre)

    print("Dosyalar başarıyla oluşturuldu!")

if __name__ == "__main__":
    liste_hazirla()
