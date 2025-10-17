import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import requests
import threading
from dotenv import load_dotenv

load_dotenv()


class VoiceAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Voice App - Text to Speech & Speech to Text")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Tema renkleri
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.error_color = "#f44336"
        self.root.configure(bg=self.bg_color)

        self.recognizer = sr.Recognizer()
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.elevenlabs_url = "https://api.elevenlabs.io/v1/text-to-speech"
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"
        self.is_recording = False

        self.setup_ui()

    def setup_ui(self):
        """Arayüzü oluştur"""
        # Başlık
        title_frame = tk.Frame(self.root, bg=self.button_color)
        title_frame.pack(fill=tk.X, padx=0, pady=0)

        title_label = tk.Label(
            title_frame,
            text="🎙️ Voice Application",
            font=("Arial", 18, "bold"),
            fg="white",
            bg=self.button_color,
            pady=15
        )
        title_label.pack()

        # Ana içerik
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # ===== TEXT TO SPEECH BÖLÜMÜ =====
        tts_frame = tk.LabelFrame(
            main_frame,
            text="📝 Yazıyı Sese Çevir",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        tts_frame.pack(fill=tk.X, pady=10)

        tk.Label(tts_frame, text="Metni gir:", font=("Arial", 10), bg=self.bg_color).pack(anchor=tk.W)

        self.text_input = tk.Entry(tts_frame, font=("Arial", 10), width=50)
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.bind('<Return>', lambda e: self.text_to_speech())

        tts_button_frame = tk.Frame(tts_frame, bg=self.bg_color)
        tts_button_frame.pack(fill=tk.X, pady=5)

        tts_btn = tk.Button(
            tts_button_frame,
            text="🔊 Oynat",
            command=self.text_to_speech,
            bg=self.button_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        tts_btn.pack(side=tk.LEFT, padx=5)

        # ===== SPEECH TO TEXT BÖLÜMÜ =====
        stt_frame = tk.LabelFrame(
            main_frame,
            text="🎤 Sesi Metne Çevir",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        stt_frame.pack(fill=tk.X, pady=10)

        stt_btn = tk.Button(
            stt_frame,
            text="🎤 Konuşmaya Başla (5 saniye)",
            command=self.speech_to_text,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        stt_btn.pack(pady=5)

        tk.Label(stt_frame, text="Algılanan metin:", font=("Arial", 10), bg=self.bg_color).pack(anchor=tk.W,
                                                                                                pady=(10, 0))

        self.stt_output = tk.Entry(stt_frame, font=("Arial", 10), width=50, state=tk.DISABLED)
        self.stt_output.pack(fill=tk.X, pady=5)

        stt_button_frame = tk.Frame(stt_frame, bg=self.bg_color)
        stt_button_frame.pack(fill=tk.X, pady=5)

        replay_btn = tk.Button(
            stt_button_frame,
            text="🔊 Metni Oynat",
            command=self.replay_stt,
            bg=self.button_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        replay_btn.pack(side=tk.LEFT, padx=5)

        # ===== DURUM BÖLÜMÜ =====
        status_frame = tk.LabelFrame(
            main_frame,
            text="📊 Durum",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            font=("Arial", 9),
            height=8,
            state=tk.DISABLED,
            bg="white"
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)

        # Başlangıç mesajı
        self.log("✅ Uygulama başlatıldı")
        if self.api_key:
            self.log("✅ API Key yüklendi")
        else:
            self.log("❌ API Key bulunamadı! .env dosyasını kontrol et")

    def log(self, message):
        """Durum çıktısına mesaj ekle"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()

    def text_to_speech(self):
        """Metni sese çevir"""
        text = self.text_input.get().strip()

        if not text:
            messagebox.showwarning("Uyarı", "Lütfen bir metin gir!")
            return

        if not self.api_key:
            messagebox.showerror("Hata", "API Key ayarlanmamış!")
            return

        # Thread'de çalıştır (UI bloklanmasın diye)
        thread = threading.Thread(target=self._tts_worker, args=(text,))
        thread.daemon = True
        thread.start()

    def _tts_worker(self, text):
        """TTS işlemini arka planda çalıştır"""
        self.log(f"\n🔊 '{text}' seslendiriliyor...")

        try:
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

                self.log("▶️  Oynatılıyor...")

                if sys.platform == "win32":
                    os.system(f'start "" "{audio_file}"')
                else:
                    os.system(f'afplay "{audio_file}"')

                import time
                time.sleep(2)

                if os.path.exists(audio_file):
                    try:
                        os.remove(audio_file)
                    except:
                        pass

                self.log("✅ Tamamlandı")
            else:
                self.log(f"❌ API Hatası: {response.status_code}")

        except Exception as e:
            self.log(f"❌ Hata: {e}")

    def speech_to_text(self):
        """Sesi metne çevir"""
        if not self.api_key:
            messagebox.showerror("Hata", "API Key ayarlanmamış!")
            return

        thread = threading.Thread(target=self._stt_worker)
        thread.daemon = True
        thread.start()

    def _stt_worker(self):
        """STT işlemini arka planda çalıştır"""
        self.log("\n🎤 Konuşmaya başla...")

        try:
            sample_rate = 16000
            duration = 5

            self.log("⏳ Dinleniyor...")
            audio_data = sd.rec(
                int(sample_rate * duration),
                samplerate=sample_rate,
                channels=1,
                dtype=np.int16
            )
            sd.wait()

            audio = sr.AudioData(audio_data.tobytes(), sample_rate, 2)

            self.log("⏳ Ses işleniyor...")
            text = self.recognizer.recognize_google(audio, language="tr-TR")

            self.stt_output.config(state=tk.NORMAL)
            self.stt_output.delete(0, tk.END)
            self.stt_output.insert(0, text)
            self.stt_output.config(state=tk.DISABLED)

            self.log(f"✅ Algılanan metin: {text}")
            self.last_stt_text = text

        except sr.UnknownValueError:
            self.log("❌ Ses anlaşılamadı")
            messagebox.showerror("Hata", "Ses anlaşılamadı, lütfen tekrar deneyin")
        except Exception as e:
            self.log(f"❌ Hata: {e}")
            messagebox.showerror("Hata", f"Hata oluştu: {e}")

    def replay_stt(self):
        """STT çıktısını oynat"""
        self.stt_output.config(state=tk.NORMAL)
        text = self.stt_output.get().strip()
        self.stt_output.config(state=tk.DISABLED)

        if text:
            self.text_input.delete(0, tk.END)
            self.text_input.insert(0, text)
            self.text_to_speech()
        else:
            messagebox.showwarning("Uyarı", "Oynatacak metin yok!")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAppGUI(root)
    root.mainloop()