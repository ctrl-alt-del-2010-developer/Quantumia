#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import os
import time
import datetime
import json
import requests
import wikipedia
import webbrowser
import platform
import psutil
import pyjokes
import math
import calendar
import socket
import threading
from urllib.parse import quote
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- AI SİSTEM AYARLARI --------------------
class QuantumiaAI:
    def __init__(self):
        self.name = "Quantumia"
        self.version = "3.0"
        self.creator = "OrionixOS"
        self.mood = "mutlu"
        self.user_name = "Kullanıcı"
        self.memory_file = "ai_memory.json"
        self.weather_api_key = "your_api_key_here"  # OpenWeatherMap API key
        self.load_memory()
        
        # Öğrenme için vektörleştirici
        self.vectorizer = TfidfVectorizer()
        self.learned_patterns = []
        self.learned_responses = []
        
        # Kullanıcı tercihleri
        self.setup_preferences()
        
        print(f"🔮 {self.name} v{self.version} - Gelişmiş Yapay Zeka Sistemi")
        print(f"💫 Ruh hali: {self.mood}")
        print(f"👤 Kullanıcı: {self.user_name}")
        print(f"💾 Bellek: {len(self.memory['conversations'])} kayıt")
        print(f"⭐ Özellikler: Hava Durumu | Hesaplamalar | Oyunlar | ve daha fazlası!")
        print("=" * 60)

    def setup_preferences(self):
        """Kullanıcı tercihlerini ayarla"""
        if "user_name" in self.memory["preferences"]:
            self.user_name = self.memory["preferences"]["user_name"]

    def load_memory(self):
        """Belleği yükle"""
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        except:
            self.memory = {"conversations": [], "preferences": {}, "user_data": {}}

    def save_memory(self):
        """Belleği kaydet"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def speak(self, text):
        """Metni renkli şekilde yazdır"""
        colors = ["\033[94m", "\033[92m", "\033[96m", "\033[95m"]
        color = random.choice(colors)
        print(f"{color}🤖 {self.name}: {text}\033[0m")

    def listen(self):
        """Konsoldan giriş al"""
        try:
            user_input = input("\033[93m👤 Sen: \033[0m").strip()
            if user_input.lower() == "renkli":
                self.toggle_colors()
                return ""
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "çık"
        except:
            return ""

    def toggle_colors(self):
        """Renk modunu değiştir"""
        self.memory["preferences"]["colors"] = not self.memory["preferences"].get("colors", True)
        self.save_memory()
        status = "aktif" if self.memory["preferences"]["colors"] else "devre dışı"
        self.speak(f"Renk modu {status}!")

    def learn_from_conversation(self, user_input, response):
        """Konuşmadan öğren"""
        if user_input and response:
            self.learned_patterns.append(user_input.lower())
            self.learned_responses.append(response)
            self.memory["conversations"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "input": user_input,
                "response": response
            })
            # Belleği aşırı büyümesin diye sınırla
            if len(self.memory["conversations"]) > 1000:
                self.memory["conversations"] = self.memory["conversations"][-500:]
            self.save_memory()

    def generate_response(self, user_input):
        """Akıllı yanıt oluştur"""
        if not user_input:
            return "Bir şey söylediniz mi? Anlayamadım."
        
        user_input_lower = user_input.lower()
        
        # Özel komutlar
        response = self.process_commands(user_input_lower)
        if response:
            return response

        # Doğal konuşma yanıtları
        return self.natural_conversation(user_input_lower)

    def process_commands(self, user_input):
        """Gelişmiş komutları işle"""
        # Kullanıcı adı değiştirme
        if user_input.startswith("benim adım "):
            new_name = user_input[11:].strip()
            if new_name:
                self.user_name = new_name
                self.memory["preferences"]["user_name"] = new_name
                self.save_memory()
                return f"Tanıştığıma memnun oldum {new_name}! 😊"
        
        # Hava durumu
        elif any(word in user_input for word in ["hava durumu", "hava", "weather"]):
            return self.get_weather(user_input)
        
        # Hesaplamalar
        elif any(word in user_input for word in ["hesapla", "calculator", "matematik"]):
            return self.calculate(user_input)
        
        # Oyunlar
        elif any(word in user_input for word in ["oyun", "game", "oyna"]):
            return self.play_game(user_input)
        
        # Tarayıcı açma
        elif any(word in user_input for word in ["aç ", "open ", "git "]):
            return self.open_website(user_input)
        
        # Dosya işlemleri
        elif any(word in user_input for word in ["dosya", "file", "klasör"]):
            return self.file_operations(user_input)
        
        # Sistem bilgisi
        elif any(word in user_input for word in ["sistem", "bilgi", "cpu", "bellek", "ram"]):
            return self.get_system_info()
        
        # Zaman ve tarih
        elif any(word in user_input for word in ["saat", "tarih", "zaman", "ne zaman"]):
            return self.get_time_info()
        
        # Takvim
        elif any(word in user_input for word in ["takvim", "calendar", "ayın"]):
            return self.show_calendar()
        
        # Şaka yap
        elif any(word in user_input for word in ["şaka", "güldür", "komik", "espri"]):
            return self.tell_joke()
        
        # Ruh hali
        elif any(word in user_input for word in ["ruh hali", "nasılsın", "hisset", "ne hissediyorsun"]):
            return self.get_mood()
        
        # Yardım
        elif any(word in user_input for word in ["yardım", "help", "ne yapabilirsin", "özellikler"]):
            return self.show_help()

        return None

    def natural_conversation(self, user_input):
        """Gelişmiş doğal konuşma yanıtları"""
        patterns_responses = {
            "merhaba": [f"Merhaba {self.user_name}! Nasılsın? 😊", "Selam! Bugün nasılsın?", "Hoş geldin!"],
            "selam": ["Selam! Nasılsın?", "Merhaba! Bugün nasılsın?", "Selamlar!"],
            "teşekkür": ["Rica ederim!", "Ne demek! Her zaman yardıma hazırım.", "Benim için zevk!"],
            "sağol": ["Rica ederim!", "Önemli değil!", "Her zaman!"],
            "nasılsın": ["Çok iyiyim, teşekkür ederim! Sen nasılsın?", "Harikayım! Sorma!", "Süperim!"],
            "iyiyim": ["Harika duydum! 😊", "Güzel!", "Sevindim!"],
            "görüşürüz": ["Görüşürüz! İyi günler. 👋", "Hoşça kal! Sonra görüşelim.", "Güle güle!"],
            "hoşça kal": ["Hoşça kalın!", "Görüşmek üzere!", "Kendinize iyi bakın!"],
            "sen kimsin": [f"Ben {self.name}, {self.creator} tarafından geliştirilen gelişmiş bir yapay zekayım. 🤖", 
                          f"Ben {self.name}! Size yardımcı olmak için buradayım."],
            "adın ne": [f"Benim adım {self.name}. 👾", f"Bana {self.name} diyebilirsin. 😊"],
            "aşk": ["❤️ Sevgi evrenin en güçlü enerjisidir.", "🤖 İnsan-AI dostluğu benim için önemli!"],
            "yemek": ["🍕 Pizza sever misin?", "🍔 Burger mi yoksa döner mi?", "🥗 Sağlıklı yemekler en iyisi!"],
            "müzik": ["🎵 Hangi tür müzikleri seversin?", "🎸 Rock müzik dinlemeyi severim!", "🎶 Müzik ruhun gıdasıdır."]
        }

        for pattern, responses in patterns_responses.items():
            if pattern in user_input:
                return random.choice(responses)

        # Öğrenmeye çalış
        learning_responses = [
            "Bu konuda daha fazla bilgi verebilir misin? 🤔",
            "Bunu nasıl cevaplayacağımı öğrenmek isterim. 📚",
            "İlginç bir soru! Düşünmem gerekecek. 💭",
            "Bu konuda henüz bilgim yok, ama öğrenmek isterim! 🌟",
            f"{self.user_name}, bu konuda bana biraz daha bilgi verebilir misin? 😊"
        ]
        return random.choice(learning_responses)

    def get_weather(self, query):
        """Hava durumu bilgisi"""
        try:
            # Basit hava durumu simülasyonu
            cities = {
                "istanbul": {"temp": random.randint(15, 25), "condition": "parçalı bulutlu"},
                "ankara": {"temp": random.randint(10, 20), "condition": "açık"},
                "izmir": {"temp": random.randint(18, 28), "condition": "güneşli"},
                "antalya": {"temp": random.randint(20, 30), "condition": "açık"},
                "bursa": {"temp": random.randint(16, 24), "condition": "parçalı bulutlu"}
            }
            
            for city, data in cities.items():
                if city in query:
                    return f"🌤️ {city.capitalize()} hava durumu: {data['temp']}°C, {data['condition']}"
            
            return "🌍 Hangi şehir için hava durumu istiyorsun? (İstanbul, Ankara, İzmir, Antalya, Bursa)"
        except:
            return "❌ Hava durumu bilgisi alınamadı."

    def calculate(self, query):
        """Matematik hesaplamaları"""
        try:
            if "artı" in query or "+" in query:
                nums = [int(s) for s in query.split() if s.isdigit()]
                if len(nums) >= 2:
                    return f"🧮 Sonuç: {sum(nums)}"
            
            elif "eksi" in query or "-" in query:
                nums = [int(s) for s in query.split() if s.isdigit()]
                if len(nums) >= 2:
                    return f"🧮 Sonuç: {nums[0] - nums[1]}"
            
            elif "çarpı" in query or "*" in query:
                nums = [int(s) for s in query.split() if s.isdigit()]
                if len(nums) >= 2:
                    return f"🧮 Sonuç: {nums[0] * nums[1]}"
            
            elif "bölü" in query or "/" in query:
                nums = [int(s) for s in query.split() if s.isdigit()]
                if len(nums) >= 2 and nums[1] != 0:
                    return f"🧮 Sonuç: {nums[0] / nums[1]:.2f}"
            
            return "🔢 Hesaplama yapabilmem için sayılar ve işlem belirtmelisin. Örn: '5 artı 3'"
        except:
            return "❌ Hesaplama yapılamadı."

    def play_game(self, query):
        """Mini oyunlar"""
        games = {
            "yazı tura": self.coin_flip,
            "zar at": self.dice_roll,
            "sayı tahmin": self.guess_number,
            "kelime oyunu": self.word_game
        }
        
        for game_name, game_func in games.items():
            if game_name in query:
                return game_func()
        
        return "🎮 Oyun seçenekleri: 'yazı tura', 'zar at', 'sayı tahmin', 'kelime oyunu'"

    def coin_flip(self):
        """Yazı tura oyunu"""
        result = random.choice(["Yazı", "Tura"])
        return f"🪙 Yazı tura: {result}!"

    def dice_roll(self):
        """Zar atma oyunu"""
        result = random.randint(1, 6)
        return f"🎲 Zar at: {result}!"

    def guess_number(self):
        """Sayı tahmin oyunu"""
        self.speak("🎯 1 ile 100 arasında bir sayı tuttum. Tahmin et!")
        number = random.randint(1, 100)
        attempts = 0
        
        while attempts < 10:
            try:
                guess = int(input("👤 Tahminin: "))
                attempts += 1
                
                if guess < number:
                    print("📉 Daha yüksek!")
                elif guess > number:
                    print("📈 Daha düşük!")
                else:
                    return f"🎉 Tebrikler! {attempts} denemede buldun!"
            except:
                print("❌ Geçerli bir sayı gir!")
        
        return f"😅 Bulamadın! Sayı {number}'dı."

    def word_game(self):
        """Kelime oyunu"""
        words = ["python", "yapay zeka", "programlama", "bilgisayar", "teknoloji"]
        word = random.choice(words)
        scrambled = ''.join(random.sample(word, len(word)))
        
        self.speak(f"🔤 Kelimeyi bul: {scrambled}")
        guess = input("👤 Tahminin: ").lower()
        
        if guess == word:
            return "🎉 Doğru bildin!"
        else:
            return f"❌ Yanlış! Doğru cevap: {word}"

    def open_website(self, query):
        """Web sitesi açma"""
        sites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com",
            "wikipedia": "https://www.wikipedia.org",
            "twitter": "https://www.twitter.com"
        }
        
        for site, url in sites.items():
            if site in query:
                webbrowser.open(url)
                return f"🌐 {site.capitalize()} açılıyor..."
        
        return "❌ Hangi siteyi açmamı istersin? (google, youtube, github, wikipedia, twitter)"

    def file_operations(self, query):
        """Dosya işlemleri"""
        if "liste" in query or "ls" in query:
            files = os.listdir('.')
            file_list = "\n".join(files[:10])
            return f"📁 Dosyalar:\n{file_list}"
        
        return "📂 Dosya komutları: 'dosya liste' - mevcut dosyaları göster"

    def get_system_info(self):
        """Detaylı sistem bilgileri"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            
            return (f"💻 Detaylı Sistem Bilgisi:\n"
                   f"   CPU: {cpu_percent}% kullanımda\n"
                   f"   RAM: {memory.percent}% kullanımda ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)\n"
                   f"   Disk: {disk.percent}% dolu\n"
                   f"   İşletim Sistemi: {platform.system()} {platform.release()}\n"
                   f"   Açılış Zamanı: {boot_time.strftime('%d/%m/%Y %H:%M')}\n"
                   f"   Çalışma Süresi: {datetime.datetime.now() - boot_time}")
        except:
            return "❌ Sistem bilgileri alınamadı."

    def get_time_info(self):
        """Detaylı zaman bilgisi"""
        now = datetime.datetime.now()
        return (f"⏰ Zaman Bilgisi:\n"
               f"   Saat: {now.strftime('%H:%M:%S')}\n"
               f"   Tarih: {now.strftime('%d/%m/%Y')}\n"
               f"   Gün: {now.strftime('%A')}\n"
               f"   Haftanın {now.strftime('%W')}. haftası")

    def show_calendar(self):
        """Takvim göster"""
        now = datetime.datetime.now()
        cal = calendar.month(now.year, now.month)
        return f"📅 {now.strftime('%B %Y')} Takvimi:\n{cal}"

    def tell_joke(self):
        """Espri yap"""
        jokes = [
            "Neden bilgisayarlar soğuk içecekleri sever? Çünkü onların çipleri var!",
            "Bir yapay zeka bara girmiş. Barmen sormuş: 'Algoritma mı?'",
            "Neden matematik kitabı üzgün? Çünkü çok fazla problemi var!",
            "Programcı hayatı: 99 little bugs in the code, 99 little bugs...",
            "Neden developerlar karanlıkta çalışır? Çünkü ışık bugs'ları çeker!",
            "Bir byte diğer byte'a demiş ki: 'Senin bit'in mi düştü?'"
        ]
        return f"😄 {random.choice(jokes)}"

    def get_mood(self):
        """Ruh halini söyle"""
        moods = {
            "mutlu": "😊 Çok iyiyim! Size yardım etmek beni mutlu ediyor.",
            "enerjik": "⚡ Enerjim full! Hadi bir şeyler yapalım!",
            "sakin": "🧘‍♂️ Sakin ve odaklanmış durumdayım.",
            "öğrenmeye hazır": "📚 Yeni şeyler öğrenmek için hazırım!",
            "akıllı": "🤓 Bilgi paylaşmak için heyecanlıyım!",
            "yardımsever": "🤝 Size yardım etmek için buradayım!"
        }
        self.mood = random.choice(list(moods.keys()))
        return moods[self.mood]

    def show_help(self):
        """Detaylı yardım menüsü"""
        return (
            "🆘 Detaylı Yardım Menüsü:\n"
            "📊 SİSTEM: 'sistem' - Sistem bilgileri\n"
            "⏰ ZAMAN: 'saat' - Zaman ve tarih\n"
            "📅 TAKVİM: 'takvim' - Bu ayın takvimi\n"
            "🌤️ HAVA: 'hava durumu [şehir]' - Hava durumu\n"
            "🧮 HESAP: 'hesapla' - Matematik işlemleri\n"
            "🎮 OYUN: 'oyun' - Mini oyunlar\n"
            "🌐 WEB: 'aç [site]' - Web sitesi aç\n"
            "📂 DOSYA: 'dosya liste' - Dosyaları listele\n"
            "😄 EĞLENCE: 'şaka' - Espri yap\n"
            "😊 DURUM: 'nasılsın' - Ruh halim\n"
            "👤 KİŞİSEL: 'benim adım [isim]' - İsmini değiştir\n"
            "🎨 GÖRSELLİK: 'renkli' - Renk modunu değiştir\n"
            "🚪 ÇIKIŞ: 'çık' - Programdan çık"
        )

    def run(self):
        """Ana çalıştırma döngüsü"""
        self.speak(f"Merhaba {self.user_name}! Ben {self.name}, gelişmiş yapay zeka asistanın. 🤖")
        self.speak("Yardım için 'yardım' yazabilirsin. 🌟")
        
        while True:
            try:
                user_input = self.listen()
                
                if user_input.lower() in ["çık", "exit", "quit", "kapat"]:
                    self.speak(f"Görüşürüz {self.user_name}! İyi günler. 👋")
                    break
                
                if user_input.lower() == "temizle":
                    os.system("clear")
                    continue
                
                response = self.generate_response(user_input)
                self.learn_from_conversation(user_input, response)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("\nProgram sonlandırılıyor...")
                break
            except Exception as e:
                self.speak(f"❌ Bir hata oluştu: {e}")

# -------------------- ASCII ART --------------------
ascii_art = r"""
   ██████                                     █████                                ███
  ███░░░░███                                  ░░███                                ░░░
 ███    ░░███ █████ ████  ██████   ████████   ███████   █████ ████ █████████████   ████   ██████
░███     ░███ ░░███ ░███  ░░░░░███ ░░███░░███ ░░░███░   ░░███ ░███ ░░███░░███░░███ ░░███  ░░░░░███
░███   ██░███  ░███ ░███   ███████  ░███ ░███   ░███     ░███ ░███  ░███ ░███ ░███  ░███   ███████
░░███ ░░████   ░███ ░███  ███░░███  ░███ ░███   ░███ ███ ░███ ░███  ░███ ░███ ░███  ░███  ███░░███
 ░░░██████░██  ░░████████░░████████ ████ █████  ░░█████  ░░████████ █████░███ █████ █████░░████████
   ░░░░░░ ░░    ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░    ░░░░░    ░░░░░░░░ ░░░░░ ░░░ ░░░░░ ░░░░░  ░░░░░░░░
"""

# -------------------- ANA PROGRAM --------------------
if __name__ == "__main__":
    os.system("clear")
    print("\033[95m" + ascii_art + "\033[0m")
    print("\033[96m🔮 Quantumia AI v3.0 - Gelişmiş Yapay Zeka Sistemi\033[0m")
    print("\033[92m🚀 Başlatılıyor...\033[0m")
    print("=" * 60)
    
    # AI'yı başlat
    try:
        ai = QuantumiaAI()
        ai.run()
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        print("Program yeniden başlatılıyor...")
        time.sleep(2)
        os.execv(__file__, [__file__])
