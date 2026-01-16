import urllib.request
import os

def guncel_sifre_al():
    """Seir-Sanduk sitesinden güncel pass anahtarını çeker."""
    try:
        # Şifre kaynağı olan link
        url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        
        # Siteye tarayıcı gibi görünmek için başlık ekliyoruz (bazı siteler botları engeller)
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            # Gelen veriyi oku ve temizle
            sifre = response.read().decode('utf-8').strip()
            print(f"✅ Güncel şifre alındı: {sifre}")
            return sifre
    except Exception as e:
        print(f"❌ Şifre alınırken bir hata oluştu: {e}")
        return None

def liste_olustur():
    sifre = guncel_sifre_al()
    
    if not sifre:
        print("HATA: Şifre alınamadığı için liste oluşturulamadı.")
        return

    # 65 Kanallık Tam Liste
    kanallar = [
        {"ad": "BNT 1 HD", "id": "hd-bnt-1-hd-online"},
        {"ad": "BNT 2", "id": "bnt-2-online"},
        {"ad": "BNT 3 HD", "id": "hd-bnt-3-hd-online"},
        {"ad": "BNT 4", "id": "bnt-4-online"},
        {"ad": "NOVA TV HD", "id": "hd-nova-tv-hd-online"},
        {"ad": "NOVA NEWS HD", "id": "hd-nova-news-hd-online"},
        {"ad": "BTV HD", "id": "hd-btv-hd-online"},
        {"ad": "BULGARIA ON AIR", "id": "bulgaria-on-air-online"},
        {"ad": "EURONEWS BULGARIA", "id": "hd-euronews-bulgaria-hd-online"},
        {"ad": "BLOOMBERG TV", "id": "bloomberg-tv-online"},
        {"ad": "BTV ACTION HD", "id": "hd-btv-action-hd-online"},
        {"ad": "BTV CINEMA", "id": "btv-cinema-online"},
        {"ad": "BTV COMEDY", "id": "hd-btv-comedy-hd-online"},
        {"ad": "BTV STORY", "id": "btv-story-online"},
        {"ad": "DIEMA", "id": "hd-diema-hd-online"},
        {"ad": "DIEMA FAMILY", "id": "hd-diema-family-hd-online"},
        {"ad": "KINO NOVA", "id": "kino-nova-online"},
        {"ad": "NAT GEO HD", "id": "hd-nat-geo-hd-online"},
        {"ad": "NAT GEO WILD HD", "id": "hd-nat-geo-wild-hd-online"},
        {"ad": "DISCOVERY CHANNEL HD", "id": "hd-discovery-channel-hd-online"},
        {"ad": "ID XTRA HD", "id": "hd-id-xtra-hd-online"},
        {"ad": "24 KITCHEN HD", "id": "hd-24-kitchen-hd-online"},
        {"ad": "STAR CRIME HD", "id": "hd-star-crime-hd-online"},
        {"ad": "STAR CHANNEL HD", "id": "hd-star-channel-hd-online"},
        {"ad": "STAR LIFE HD", "id": "hd-star-life-hd-online"},
        {"ad": "EUROSPORT 1 HD", "id": "hd-eurosport-1-hd-online"},
        {"ad": "EUROSPORT 2 HD", "id": "hd-eurosport-2-hd-online"},
        {"ad": "DIEMA SPORT HD", "id": "hd-diema-sport-hd-online"},
        {"ad": "DIEMA SPORT 2 HD", "id": "hd-diema-sport-2-hd-online"},
        {"ad": "DIEMA SPORT 3 HD", "id": "hd-diema-sport-3-hd-online"},
        {"ad": "MAX SPORT 1 HD", "id": "hd-max-sport-1-hd-online"},
        {"ad": "MAX SPORT 2 HD", "id": "hd-max-sport-2-hd-online"},
        {"ad": "MAX SPORT 3 HD", "id": "hd-max-sport-3-hd-online"},
        {"ad": "MAX SPORT 4 HD", "id": "hd-max-sport-4-hd-online"},
        {"ad": "RING BG HD", "id": "hd-ring-bg-hd-online"},
        {"ad": "NOVA SPORT HD", "id": "hd-nova-sport-hd-online"},
        {"ad": "PLANETA HD", "id": "hd-planeta-hd-online"},
        {"ad": "DSTV", "id": "dstv-online"},
        {"ad": "FOLKLOR TV", "id": "folklor-tv-online"},
        {"ad": "PLANETA FOLK", "id": "planeta-folk-online"},
        {"ad": "RODINA TV", "id": "rodina-tv-online"},
        {"ad": "TIANKOV TV", "id": "tiankov-tv-online"},
        {"ad": "CITY TV", "id": "city-tv-online"},
        {"ad": "THE VOICE", "id": "the-voice-online"},
        {"ad": "TLC", "id": "tlc-online"},
        {"ad": "TRAVEL CHANNEL HD", "id": "hd-travel-channel-hd-online"},
        {"ad": "TRAVEL TV", "id": "travel-tv-online"},
        {"ad": "EVROKOM", "id": "evrokom-online"},
        {"ad": "78 TV HD", "id": "hd-78-tv-hd-online"},
        {"ad": "KANAL 3", "id": "kanal-3-online"},
        {"ad": "SKAT", "id": "skat-online"},
        {"ad": "TV 1", "id": "tv-1-online"},
        {"ad": "VTK", "id": "vtk-online"},
        {"ad": "AXN", "id": "axn-online"},
        {"ad": "AXN BLACK", "id": "axn-black-online"},
        {"ad": "AXN WHITE", "id": "axn-white-online"},
        {"ad": "EPIC DRAMA HD", "id": "hd-epic-drama-hd-online"},
        {"ad": "CODE FASHION TV HD", "id": "hd-code-fashion-tv-hd-online"},
        {"ad": "CARTOON NETWORK", "id": "cartoon-network-online"},
        {"ad": "DISNEY CHANNEL", "id": "hd-disney-channel-hd-online"},
        {"ad": "E KIDS", "id": "e-kids-online"},
        {"ad": "FOOD NETWORK HD", "id": "hd-food-network-hd-online"},
        {"ad": "NICK JR", "id": "nick-jr-online"},
        {"ad": "NICKELODEON", "id": "nickelodeon-online"},
        {"ad": "NICKTOONS", "id": "nicktoons-online"}
    ]

    m3u_icerik = "#EXTM3U\n"
    
    for k in kanallar:
        # Link yapısı workers üzerinden kuruluyor
        link = f"http://tv.seirsanduk.workers.dev/?ID=https://www.seir-sanduk.com/{k['id']}?pass={sifre}"
        m3u_icerik += f"#EXTINF:-1,{k['ad']}\n{link}\n"

    # Dosyayı kaydet
    with open("bulgar_iptv.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"🚀 BAŞARILI: {len(kanallar)} kanallı 'bulgar_iptv.m3u' dosyası oluşturuldu.")

if __name__ == "__main__":
    liste_olustur()
