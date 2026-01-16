import os

def liste_olustur():
    # Forumdan aldığın şifreyi aşağıdaki tırnakların içine yapıştır
    guncel_sifre = "BURAYA_SIFREYI_YAZ"
    
    # Kanal Listesi
    kanallar = [
        {"ad": "bTV HD", "id": "hd-btv-hd"},
        {"ad": "Nova TV", "id": "nova-tv"},
        {"ad": "Diema Sport", "id": "diema-sport-hd"}
    ]
    
    m3u_icerik = "#EXTM3U\n"
    
    for kanal in kanallar:
        link = f"https://www.seir-sanduk.com/?player=11&id={kanal['id']}&pass={guncel_sifre}"
        m3u_icerik += f"#EXTINF:-1,{kanal['ad']}\n{link}\n"
    
    # Dosyayı kaydet
    with open("liste.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print("Liste başarıyla güncellendi!")

if __name__ == "__main__":
    liste_olustur()
