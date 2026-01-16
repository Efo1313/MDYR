import os

def liste_olustur():
    # Şifre otomatik yönetildiği için buraya sabit şifre yazmamıza gerek kalmayabilir
    # Ama biz yine de en son çalışan şifreyi ekleyelim
    sifre = "11kalAdKaAde11sF8F01011616011601"
    
    # Tüm TV kanallarının ID listesi
    kanallar = [
        {"ad": "BNT 1 HD", "id": "hd-bnt-1-hd"},
        {"ad": "BTV HD", "id": "hd-btv-hd"},
        {"ad": "NOVA TV HD", "id": "nova-tv-hd"},
        {"ad": "DIEMA SPORT HD", "id": "diema-sport-hd"},
        {"ad": "DIEMA SPORT 2 HD", "id": "diema-sport-2-hd"},
        {"ad": "MAX SPORT 1 HD", "id": "max-sport-1-hd"},
        {"ad": "MAX SPORT 2 HD", "id": "max-sport-2-hd"},
        {"ad": "HBO HD", "id": "hbo-hd-bg"}
    ]

    m3u_icerik = "#EXTM3U\n"
    
    for k in kanallar:
        # Senin paylaştığın workers yapısını kullanarak link oluşturuyoruz
        # Bu yapı şifre patlasa bile yönlendirme sayesinde yayını korumaya çalışır
        link = f"http://tv.seirsanduk.workers.dev/?ID=https%3A%2F%2Fwww.seir-sanduk.com%2F%3Fplayer%3D11%26id%3D{k['id']}%26pass%3D{sifre}"
        m3u_icerik += f"#EXTINF:-1,{k['ad']}\n{link}\n"

    with open("liste.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print("M3U Listesi Workers desteğiyle oluşturuldu!")

if __name__ == "__main__":
    liste_olustur()
