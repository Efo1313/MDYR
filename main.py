name: Sifre Guncelleyici

on:
  schedule:
    - cron: '0 * * * *' # Her saat başı çalışır
  workflow_dispatch:      # İstediğinde elle başlatman için

permissions:
  contents: write         # GitHub'ın dosyayı kaydedebilmesi için gerekli izin

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Kodlari Cek
        uses: actions/checkout@v3

      - name: Python Kur
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Kütüphaneleri Kur
        run: pip install requests beautifulsoup4

      - name: Kodu Calistir
        run: python main.py  # Burayı küçük harf 'main.py' yaptık

      - name: Degisiklikleri Kaydet
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add sifre.txt link.txt || exit 0
          git commit -m "Sifre guncellendi: $(date)" || exit 0
          git push
