import os

def liste_olustur():
    # Eğer site botu engellerse, şifreyi manuel olarak buradan veya 
    # GitHub Secrets kısmından alabiliriz. 
    # Şimdilik senin paylaştığın son çalışan şifreyi varsayılan yapalım.
    
    varsayilan_sifre = "11kalAdKaAde11sF8F01011616011601"
    
    # Dosyaları her halükarda oluştur ki hata vermesin
    try:
        with open("sifre.txt", "w") as f:
            f.write(varsayilan_sifre)
            
        m3u_icerik = f"#EXTM3U\n#EXTINF:-1,Seir Sanduk TV\nhttps://www.seir-sanduk.com/?player=11&id=hd-btv-hd&pass={varsayilan_sifre}"
        
        with open("liste.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
            
        print("Dosyalar başarıyla oluşturuldu ve yüklenebilir hale getirildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    liste_olustur()
