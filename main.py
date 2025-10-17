import os
import sys
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import requests
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()


class VoiceApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"
        print("✅ Uygulama başlatıldı (ElevenLabs TTS + Google STT)\n")

    def speech_to_text(self):
        """Mikrofondan ses kaydı al ve metne çevir"""
        print("\n🎤 Konuş (5 saniye)...")

        try:
            # Mikrofon ile 5 saniye ses kaydet
            sample_rate = 16000
            duration = 5

            print("⏳ Dinleniyor...")
            audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
            sd.wait()

            # Ses dosyasına çevir
            audio = sr.AudioData(audio_data.tobytes(), sample_rate, 2)

            print("⏳ Ses işleniyor...")
            text = self.recognizer.recognize_google(audio, language="tr-TR")
            print(f"✅ Algılanan metin: {text}")
            return text

        except sr.UnknownValueError:
            print("❌ Ses anlaşılamadı, lütfen tekrar deneyin")
            return None
        except sr.RequestError as e:
            print(f"❌ Hata: {e}")
            return None
        except Exception as e:
            print(f"❌ Hata: {e}")
            return None

    def text_to_speech(self, text):
        """ElevenLabs API ile metni gerçekçi sese çevir"""
        print(f"\n🔊 '{text}' seslendiriliyor...")

        if not self.api_key:
            print("❌ ELEVENLABS_API_KEY ayarlanmamış!")
            return False

        try:
            import time

            headers = {
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }

            payload = {
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(
                f"{self.elevenlabs_url}/{self.voice_id}",
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                audio_file = "output_audio.mp3"
                with open(audio_file, "wb") as f:
                    f.write(response.content)

                print("▶️  Oynatılıyor...")

                # Windows'ta varsayılan oynatıcı
                if sys.platform == "win32":
                    os.system(f'start "" "{audio_file}"')
                else:
                    os.system(f'afplay "{audio_file}"')

                time.sleep(2)

                if os.path.exists(audio_file):
                    try:
                        os.remove(audio_file)
                    except:
                        pass

                return True
            else:
                print(f"❌ API Hatası: {response.status_code}")
                print(response.text)
                return False

        except Exception as e:
            print(f"❌ Hata: {e}")
            return False

    def run(self):
        """Uygulamayı çalıştır"""
        print("=" * 50)
        print("🎙️  TEXT-TO-SPEECH & SPEECH-TO-TEXT APP")
        print("=" * 50)

        while True:
            print("\n1. Yazıyı sese çevir")
            print("2. Sesi metne çevir")
            print("3. Çıkış")

            choice = input("\nSeçim yapın (1-3): ").strip()

            if choice == "1":
                text = input("Metni girin: ").strip()
                if text:
                    self.text_to_speech(text)

            elif choice == "2":
                result = self.speech_to_text()
                if result:
                    play_back = input("Metni geri oynatmak ister misin? (e/h): ").lower()
                    if play_back == "e":
                        self.text_to_speech(result)

            elif choice == "3":
                print("👋 Hoşça kalın!")
                break

            else:
                print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    app = VoiceApp()
    app.run()