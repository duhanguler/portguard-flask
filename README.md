# PortGuard

PortGuard, IP ve port'ların durumunu gerçek zamanlı takip eden, kullanıcı girişli, grafik arayüzlü ve Telegram bildirim destekli bir Flask uygulamasıdır.

## Özellikler

- Gerçek zamanlı port kontrolü
- Kullanıcı giriş sistemi (SQLite)
- Uptime yüzdesi için grafik (Chart.js)
- Modern Bootstrap arayüz
- Telegram bot ile kapalı port bildirimi
- Docker ve docker-compose desteği

## Kurulum

1. Depoyu klonlayın:
   git clone https://github.com/kullanici-adi/portguard.git
   cd portguard

2. Bağımlılıkları yükleyin:
   pip install -r requirements.txt

3. config.json dosyasını düzenleyin:
{
  "targets": [
    {"ip": "1.1.1.1", "port": 80},
    {"ip": "8.8.8.8", "port": 53}
  ],
  "telegram": {
    "token": "BOT_TOKENINIZ",
    "chat_id": "CHAT_ID"
  }
}

4. Uygulamayı başlatın:
   python app.py

## Docker ile Çalıştırmak için

1. Docker Compose başlatın:
   docker-compose up --build -d

2. Uygulamaya erişin:
   http://localhost:5000

## Kullanıcı Bilgileri

Varsayılan kullanıcı adı: admin  
Varsayılan şifre: admin

## Dosya Yapısı

- app.py
- config.json
- logs.db
- requirements.txt
- Dockerfile
- docker-compose.yml
- templates/
- static/

## Lisans

MIT
