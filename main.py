import urllib.request
import os

def guncel_sifre_al():
    try:
        url = "https://www.seir-sanduk.com/linkzagledane.php?parola=FaeagaDs3AdKaAf9"
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8').strip()
    except:
        return None

def liste_olustur():
    sifre = guncel_sifre_al()
    if not sifre:
        print("Sifre alinamadi!")
        return

    # Tam 65 Kanallık ID Listesi
    kanal_datalari = [
        ("BNT 1 HD", "hd-bnt-1-hd-online"), ("BNT 2", "bnt-2-online"), ("BNT 3 HD", "hd-bnt-3-hd-online"),
        ("BNT 4", "bnt-4-online"), ("NOVA TV HD", "hd-nova-tv-hd-online"), ("NOVA NEWS HD", "hd-nova-news-hd-online"),
        ("BTV HD", "hd-btv-hd-online"), ("BULGARIA ON AIR", "bulgaria-on-air-online"), ("EURONEWS BULGARIA", "hd-euronews-bulgaria-hd-online"),
        ("BLOOMBERG TV", "bloomberg-tv-online"), ("BTV ACTION HD", "hd-btv-action-hd-online"), ("BTV CINEMA", "btv-cinema-online"),
        ("BTV COMEDY", "hd-btv-comedy-hd-online"), ("BTV STORY", "btv-story-online"), ("DIEMA", "hd-diema-hd-online"),
        ("DIEMA FAMILY", "hd-diema-family-hd-online"), ("KINO NOVA", "kino-nova-online"), ("NAT GEO HD", "hd-nat-geo-hd-online"),
        ("NAT GEO WILD HD", "hd-nat-geo-wild-hd-online"), ("DISCOVERY CHANNEL HD", "hd-discovery-channel-hd-online"),
        ("ID XTRA HD", "hd-id-xtra-hd-online"), ("24 KITCHEN HD", "hd-24-kitchen-hd-online"), ("STAR CRIME HD", "hd-star-crime-hd-online"),
        ("STAR CHANNEL HD", "hd-star-channel-hd-online"), ("STAR LIFE HD", "hd-star-life-hd-online"), ("EUROSPORT 1 HD", "hd-eurosport-1-hd-online"),
        ("EUROSPORT 2 HD", "hd-eurosport-2-hd-online"), ("DIEMA SPORT HD", "hd-diema-sport-hd-online"), ("DIEMA SPORT 2 HD", "hd-diema-sport-2-hd-online"),
        ("DIEMA SPORT 3 HD", "hd-diema-sport-3-hd-online"), ("MAX SPORT 1 HD", "hd-max-sport-1-hd-online"), ("MAX SPORT 2 HD", "hd-max-sport-2-hd-online"),
        ("MAX SPORT 3 HD", "hd-max-sport-3-hd-online"), ("MAX SPORT 4 HD", "hd-max-sport-4-hd-online"), ("RING BG HD", "hd-ring-bg-hd-online"),
        ("NOVA SPORT HD", "hd-nova-sport-hd-online"), ("PLANETA HD", "hd-planeta-hd-online"), ("DSTV", "dstv-online"),
        ("FOLKLOR TV", "folklor-tv-online"), ("PLANETA FOLK", "planeta-folk-online"), ("RODINA TV", "rodina-tv-online"),
        ("TIANKOV TV", "tiankov-tv-online"), ("CITY TV", "city-tv-online"), ("THE VOICE", "the-voice-online"),
        ("TLC", "tlc-online"), ("TRAVEL CHANNEL HD", "hd-travel-channel-hd-online"), ("TRAVEL TV", "travel-tv-online"),
        ("EVROKOM", "evrokom-online"), ("78 TV HD", "hd-78-tv-hd-online"), ("KANAL 3", "kanal-3-online"),
        ("SKAT", "skat-online"), ("TV 1", "tv-1-online"), ("VTK", "vtk-online"), ("AXN", "axn-online"),
        ("AXN BLACK", "axn-black-online"), ("AXN WHITE", "axn-white-online"), ("EPIC DRAMA HD", "hd-epic-drama-hd-online"),
        ("CODE FASHION TV HD", "hd-code-fashion-tv-hd-online"), ("CARTOON NETWORK", "cartoon-network-online"),
        ("DISNEY CHANNEL", "hd-disney-channel-hd-online"), ("E KIDS", "e-kids-online"), ("FOOD NETWORK HD", "hd-food-network-hd-online"),
        ("NICK JR", "nick-jr-online"), ("NICKELODEON", "nickelodeon-online"), ("NICKTOONS", "nicktoons-online")
    ]

    m3u_icerik = "#EXTM3U\n"
    for ad, id_kod in kanal_datalari:
        link = f"http://tv.seirsanduk.workers.dev/?ID=https://www.seir-sanduk.com/{id_kod}?pass={sifre}"
        m3u_icerik += f"#EXTINF:-1,{ad}\n{link}\n"

    # DOSYA ADI: liste.m3u
    with open("liste.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    print("M3U dosyasi basariyla olusturuldu.")

if __name__ == "__main__":
    liste_olustur()
