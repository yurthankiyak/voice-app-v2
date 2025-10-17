# 🎙️ Text-to-Speech & Speech-to-Text Mini App

Python ile yazılmış, **gerçekçi ses kalitesine** sahip metin-konuşma ve konuşma-metin çevirme uygulaması.

## 🌟 Özellikler

✅ **Text-to-Speech (TTS)**: Metni doğal, gerçekçi sese çevir  
✅ **Speech-to-Text (STT)**: Konuşmayı metne çevir  
✅ **Türkçe Desteği**: Tam Türkçe dil desteği  
✅ **Gerçekçi Ses**: ElevenLabs API ile insan gibi ses  
✅ **Kolay Kullanım**: GUI arayüzü ile basit kontrol  

---

## 📋 Sistem Gereksinimleri

- Python 3.8 veya üstü
- Mikrofon (Speech-to-Text için)
- Hoparlör (Text-to-Speech için)
- İnternet bağlantısı

---

## 🚀 Kurulum

### Adım 1: Repoyu İndir
```bash
git clone https://github.com/yurthankiyak/voice-app-v2.git
cd voice-app-v2
```

### Adım 2: Sanal Ortam Oluştur (İsteğe Bağlı)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Adım 3: Kütüphaneleri Kur
```bash
pip install -r requirements.txt
```

### Adım 4: ElevenLabs API Key Alma
1. https://elevenlabs.io adresine git
2. Ücretsiz hesap oluştur (ayda 10,000 karakter)
3. Dashboard'dan API Key'i kopyala

### Adım 5: .env Dosyası Oluştur
Proje klasöründe `.env` dosyası oluştur:
```
ELEVENLABS_API_KEY=your_api_key_here
```

---

## 💻 Nasıl Kullanılır?

### 🖥️ GUI Arayüzü ile (Önerilen)
```bash
python main.py
```

Açılan pencerede:
1. **📝 Yazıyı Sese Çevir:** Metni gir → "🔊 Oynat" butonuna tıkla
2. **🎤 Sesi Metne Çevir:** "🎤 Konuşmaya Başla" butonuna tıkla, 5 saniye konuş
3. **🔊 Metni Oynat:** Algılanan metni seslendir

### Özellikler
- ✨ Görsel ve kolay arayüz
- 🔄 Gerçek zamanlı durum güncellemeleri
- 🎵 Anında ses oynatma
- 📋 Tüm işlemler kaydedilir

---

## 📁 Proje Yapısı

```
voice-app-v2/
├── main.py                 # GUI uygulaması
├── .env                    # API Key (git tarafından görmezden gelinir)
├── .gitignore              # Git'in izlemesini istemediğimiz dosyalar
├── requirements.txt        # Kütüphane bağımlılıkları
├── README.md               # Bu dosya
└── output_audio.mp3        # Geçici ses dosyası (otomatik silinir)
```

---

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

| Teknoloji | Kullanım |
|-----------|----------|
| **SpeechRecognition** | Konuşmayı metne çevirme (Google Cloud API) |
| **ElevenLabs API** | Gerçekçi metin-konuşma sentezi |
| **sounddevice** | Mikrofon ses kaydı |
| **numpy** | Ses verisi işleme |
| **requests** | API iletişimi |
| **python-dotenv** | Ortam değişkenleri yönetimi |

### Ses Kalitesi

Varsayılan ses: **Adam Sesi (Profesyonel)**
- Voice ID: `21m00Tcm4TlvDq8ikWAM`
- Doğal ve akıcı yapay ses
- ElevenLabs'in en iyi seslerinden biri

Başka sesler için `main.py` içinde `self.voice_id` değerini değiştirebilirsin.

---

## 🛠️ Sorun Giderme

### ❌ "ELEVENLABS_API_KEY ayarlanmamış" hatası
**Çözüm:** `.env` dosyasının proje klasöründe olduğundan emin ol
```bash
# Windows
dir /a | find ".env"

# macOS/Linux
ls -la | grep .env
```

### ❌ Mikrofon çalışmıyor
**Çözüm:** Sisteminizde hangi mikrofonlar var kontrol et
```bash
python -c "import sounddevice as sd; print(sd.query_devices())"
```

### ❌ Ses oynatılmıyor
**Çözüm:** Hoparförün ses düzeyini kontrol et, Windows'ta Media Player yüklü olmalı

### ❌ "pip: command not found" hatası
**Çözüm:** Python doğru kurulu değil, yeniden kur veya PATH'e ekle

---

## 📊 API Kullanımı

### ElevenLabs
- **Ücretsiz Plan:** Ayda 10,000 karakter
- **Ücretli Plan:** Daha fazla karakter ve premium sesler
- **Detaylar:** https://elevenlabs.io/pricing

### Google Cloud Speech-to-Text
- **Ücretsiz:** Ayda 60 dakika
- **Ücretli:** Daha fazla dakika

---

## 🔒 Güvenlik

✅ `.env` dosyası Git tarafından takip edilmez (API Key korunur)  
✅ Geçici ses dosyaları otomatik silinir  
✅ Hassas bilgiler kodda saklanmaz  

**API Key'i asla GitHub'a commit etme!**

---

## 📝 Lisans

MIT License - Özgürce kullan ve değiştir

---

## 👨‍💻 Geliştirici

**Yurth Ankıyak**

---

## 🤝 İyileştirme Önerileri

Hocalardan gelen öneriler:
- [ ] Farklı dillere destek ekle
- [ ] GUI arayüz yap (Tkinter/PyQt)
- [ ] Ses dosyası kaydetme özelliği
- [ ] Batch işleme (birden fazla dosya)
- [ ] Ses dosyasından metin çevirme

---

## 📞 İletişim & Sorular

Soruların varsa:
1. GitHub Issues açabilirsin
2. Repo'ya Pull Request gönderebilirsin

---

## ✨ Test Edildi

✅ Windows 10/11  
✅ Python 3.8+  
✅ Türkçe konuşma tanıma  
✅ ElevenLabs API entegrasyonu  

---

**Başarılar! 🚀**
