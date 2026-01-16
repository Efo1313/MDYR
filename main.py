import requests
from bs4 import BeautifulSoup
import re

def sifreyi_al():
    # Şifrenin yayınlandığı ana sayfa veya şifre alma sayfası
    url = "https://www.seir-sanduk.com/" 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Bağlantı hatası varsa uyarır
        
        # Sayfa içeriğini analiz et
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # YÖNTEM A: Şifre bir input içindeyse (Örn: <input id="pass" value="...">)
        # Sitedeki doğru ID'yi bulmanız gerekir
        pass_element = soup.find('input', {'id': 'pass'}) 
        
        if pass_element:
            return pass_element['value']
        
        # YÖNTEM B: Şifre metin içindeyse (Düzenli ifade ile arama)
        # Genellikle 32 karakterli karmaşık bir dizin olur
        match = re.search(r'pass=([a-zA-Z0-9]{20,})', response.text)
        if match:
            return match.group(1)

        return "Şifre bulunamadı, sitenin HTML yapısı değişmiş olabilir."

    except Exception as e:
        return f"Hata oluştu: {e}"

# Kullanım
guncel_pass = sifreyi_al()
print(f"Güncel Şifreniz: {guncel_pass}")
print(f"Tam Link: https://www.seir-sanduk.com/?pass={guncel_pass}")
