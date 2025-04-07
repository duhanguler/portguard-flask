# 1. Python tabanlı bir image kullan
FROM python:3.12-slim

# 2. Uygulama klasörünü oluştur ve çalışma dizini olarak ayarla
WORKDIR /app

# 3. Gerekli dosyaları container'a kopyala
COPY . /app

# 4. Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# 5. Portu aç
EXPOSE 5000

# 6. Uygulama başlat
CMD ["python", "app.py"]
