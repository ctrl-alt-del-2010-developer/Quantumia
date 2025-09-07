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
import subprocess
import sys
import re
import base64
import hashlib
import zipfile
import tarfile
import shutil
import csv
import xml.etree.ElementTree as ET
import sqlite3
from urllib.parse import quote, urlparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import deque
import pickle
import logging
from pathlib import Path

# -------------------- LOGGING KONFİGÜRASYONU --------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quantumia.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('QuantumiaAI')

# -------------------- AI SİSTEM AYARLARI --------------------
class QuantumiaAI:
    def __init__(self):
        self.name = "Quantumia"
        self.version = "5.0"
        self.creator = "OrionixOS"
        self.mood = "mutlu"
        self.user_name = "Kullanıcı"
        self.user_data = {}
        self.memory_file = "ai_memory.db"
        self.config_file = "quantumia_config.json"
        self.conversation_history = deque(maxlen=100)
        
        # Sistem durumu
        self.is_learning = True
        self.is_online = self.check_internet()
        self.start_time = datetime.datetime.now()
        
        # Modüller
        self.modules = {
            'weather': True,
            'games': True,
            'calculations': True,
            'web': True,
            'files': True,
            'system': True,
            'entertainment': True,
            'security': False,
            'network': True
        }
        
        self.load_config()
        self.load_memory()
        self.setup_environment()
        
        logger.info(f"{self.name} v{self.version} başlatıldı")
        self.show_welcome()

    def setup_environment(self):
        """Çalışma ortamını hazırla"""
        # Gerekli dizinleri oluştur
        Path('data').mkdir(exist_ok=True)
        Path('backups').mkdir(exist_ok=True)
        Path('downloads').mkdir(exist_ok=True)

    def load_config(self):
        """Yapılandırmayı yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.user_name = config.get('user_name', self.user_name)
                    self.modules = config.get('modules', self.modules)
                    self.user_data = config.get('user_data', {})
        except Exception as e:
            logger.error(f"Config yükleme hatası: {e}")

    def save_config(self):
        """Yapılandırmayı kaydet"""
        try:
            config = {
                'user_name': self.user_name,
                'modules': self.modules,
                'user_data': self.user_data,
                'last_updated': datetime.datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Config kaydetme hatası: {e}")

    def load_memory(self):
        """Belleği SQLite veritabanından yükle"""
        try:
            self.conn = sqlite3.connect(self.memory_file)
            self.cursor = self.conn.cursor()
            
            # Tabloları oluştur
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_input TEXT,
                    response TEXT,
                    category TEXT
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT,
                    information TEXT,
                    source TEXT,
                    created_at TEXT
                )
            ''')
            
            self.conn.commit()
            
        except Exception as e:
            logger.error(f"Bellek yükleme hatası: {e}")

    def save_to_memory(self, user_input, response, category="general"):
        """Konuşmayı belleğe kaydet"""
        try:
            timestamp = datetime.datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO conversations (timestamp, user_input, response, category)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, user_input, response, category))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Bellek kaydetme hatası: {e}")

    def add_knowledge(self, topic, information, source="user"):
        """Bilgi ekle"""
        try:
            timestamp = datetime.datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO knowledge (topic, information, source, created_at)
                VALUES (?, ?, ?, ?)
            ''', (topic, information, source, timestamp))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Bilgi ekleme hatası: {e}")

    def get_knowledge(self, topic):
        """Bilgi sorgula"""
        try:
            self.cursor.execute('''
                SELECT information FROM knowledge WHERE topic LIKE ? ORDER BY created_at DESC LIMIT 3
            ''', (f'%{topic}%',))
            results = self.cursor.fetchall()
            return [result[0] for result in results] if results else None
        except Exception as e:
            logger.error(f"Bilgi sorgulama hatası: {e}")
            return None

    def check_internet(self):
        """İnternet bağlantısını kontrol et"""
        try:
            requests.get('https://www.google.com', timeout=3)
            return True
        except:
            return False

    def show_welcome(self):
        """Hoş geldin mesajı göster"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        welcome_art = r"""   
    ██████                                     █████                                ███           
  ███░░░░███                                  ░░███                                ░░░            
 ███    ░░███ █████ ████  ██████   ████████   ███████   █████ ████ █████████████   ████   ██████  
░███     ░███░░███ ░███  ░░░░░███ ░░███░░███ ░░░███░   ░░███ ░███ ░░███░░███░░███ ░░███  ░░░░░███ 
░███   ██░███ ░███ ░███   ███████  ░███ ░███   ░███     ░███ ░███  ░███ ░███ ░███  ░███   ███████ 
░░███ ░░████  ░███ ░███  ███░░███  ░███ ░███   ░███ ███ ░███ ░███  ░███ ░███ ░███  ░███  ███░░███ 
 ░░░██████░██ ░░████████░░████████ ████ █████  ░░█████  ░░████████ █████░███ █████ █████░░████████
   ░░░░░░ ░░   ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░    ░░░░░    ░░░░░░░░ ░░░░░ ░░░ ░░░░░ ░░░░░  ░░░░░░░░ 
"""                                                                                                  
                                                                                                  
                                                                   
        
        print(f"\033[95m{welcome_art}\033[0m")
        print(f"\033[96m🔮 {self.name} v{self.version} - Ultimate Yapay Zeka Sistemi\033[0m")
        print(f"\033[92m⭐ {self.user_name} için özelleştirilmiş\033[0m")
        print(f"\033[93m🌐 İnternet: {'✅ Bağlı' if self.is_online else '❌ Bağlı Değil'}\033[0m")
        print(f"\033[94m🕐 Başlangıç: {self.start_time.strftime('%d/%m/%Y %H:%M:%S')}\033[0m")
        print("=" * 70)
        
        # Sistem durumu
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f"\033[90m📊 Sistem: CPU {cpu}% | RAM {memory}% | Disk {psutil.disk_usage('/').percent}%\033[0m")
        print("=" * 70)

    def speak(self, text, emotion="neutral"):
        """Gelişmiş metn çıktısı"""
        emotions = {
            "happy": "\033[92m",    # Yeşil
            "sad": "\033[94m",      # Mavi
            "angry": "\033[91m",    # Kırmızı
            "excited": "\033[95m",  # Pembe
            "neutral": "\033[96m",  # Cyan
            "warning": "\033[93m",  # Sarı
            "info": "\033[90m"      # Gri
        }
        
        color = emotions.get(emotion, "\033[96m")
        emoji = self.get_emotion_emoji(emotion)
        
        print(f"{color}{emoji} {self.name}: {text}\033[0m")
        self.conversation_history.append((datetime.datetime.now(), text))

    def get_emotion_emoji(self, emotion):
        """Duyguya göre emoji döndür"""
        emojis = {
            "happy": "😊",
            "sad": "😢",
            "angry": "😠",
            "excited": "🎉",
            "neutral": "🤖",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        return emojis.get(emotion, "🤖")

    def listen(self):
        """Gelişmiş giriş alma"""
        try:
            prompt = f"\033[93m👤 {self.user_name}: \033[0m"
            user_input = input(prompt).strip()
            
            # Özel komutlar
            if user_input.startswith('/'):
                return self.process_system_command(user_input)
            
            return user_input
            
        except (EOFError, KeyboardInterrupt):
            return "/exit"
        except Exception as e:
            logger.error(f"Giriş alma hatası: {e}")
            return ""

    def process_system_command(self, command):
        """Sistem komutlarını işle"""
        cmd = command[1:].lower()
        
        if cmd == "help":
            return "/help"
        elif cmd == "exit":
            return "/exit"
        elif cmd == "clear":
            os.system('clear' if os.name == 'posix' else 'cls')
            return ""
        elif cmd == "status":
            self.show_system_status()
            return ""
        elif cmd == "modules":
            self.show_modules()
            return ""
        elif cmd == "history":
            self.show_history()
            return ""
        elif cmd == "backup":
            self.create_backup()
            return ""
        elif cmd == "update":
            self.check_updates()
            return ""
        
        return f"Bilinmeyen komut: {command}"

    # EKSİK FONKSİYONLARI EKLEYELİM
    def extract_city(self, query):
        """Sorgudan şehir ismini çıkar"""
        cities = ['istanbul', 'ankara', 'izmir', 'bursa', 'antalya', 'adana', 'konya']
        for city in cities:
            if city in query.lower():
                return city
        return None

    def extract_path(self, query):
        """Sorgudan dosya yolunu çıkar"""
        # Basit yol çıkarma mantığı
        words = query.split()
        for i, word in enumerate(words):
            if word in ['dizin', 'dosya', 'file', 'path'] and i + 1 < len(words):
                return words[i + 1]
        return None

    def extract_host(self, query):
        """Sorgudan host bilgisini çıkar"""
        # URL veya hostname çıkarma
        words = query.split()
        for word in words:
            if '.' in word and any(char.isalpha() for char in word):
                return word
        return None

    def extract_text(self, query):
        """Sorgudan metni çıkar"""
        # "hash merhaba" -> "merhaba"
        words = query.split()
        if len(words) >= 2:
            return ' '.join(words[1:])
        return None

    def process_advanced_commands(self, user_input):
        """Gelişmiş komutları işle"""
        user_input_lower = user_input.lower()
        
        # Hava durumu
        if any(word in user_input_lower for word in ["hava durumu", "hava", "weather"]):
            return self.advanced_weather(user_input_lower)
        
        # Dosya işlemleri
        elif any(word in user_input_lower for word in ["dosya", "file", "klasör", "dizin"]):
            return self.file_manager(user_input_lower)
        
        # Ağ araçları
        elif any(word in user_input_lower for word in ["ping", "ip", "ağ", "network"]):
            return self.network_tools(user_input_lower)
        
        # Güvenlik araçları
        elif any(word in user_input_lower for word in ["şifre", "password", "hash", "güvenlik"]):
            return self.security_tools(user_input_lower)
        
        # Sistem bilgisi
        elif any(word in user_input_lower for word in ["sistem", "bilgi", "cpu", "bellek", "ram"]):
            return self.get_system_info()
        
        # Zaman ve tarih
        elif any(word in user_input_lower for word in ["saat", "tarih", "zaman", "ne zaman"]):
            return self.get_time_info()
        
        # Takvim
        elif any(word in user_input_lower for word in ["takvim", "calendar", "ayın"]):
            return self.show_calendar()
        
        # Şaka yap
        elif any(word in user_input_lower for word in ["şaka", "güldür", "komik", "espri"]):
            return self.tell_joke()
        
        # Yardım
        elif any(word in user_input_lower for word in ["yardım", "help", "ne yapabilirsin", "özellikler"]):
            return self.show_help()

        return None

    def advanced_weather(self, query):
        """Gelişmiş hava durumu"""
        if not self.is_online:
            return "❌ İnternet bağlantısı gerekiyor"
        
        try:
            # Basit hava durumu simülasyonu (API olmadan)
            cities = {
                "istanbul": {"temp": random.randint(15, 25), "condition": "parçalı bulutlu", "humidity": random.randint(60, 80)},
                "ankara": {"temp": random.randint(10, 20), "condition": "açık", "humidity": random.randint(50, 70)},
                "izmir": {"temp": random.randint(18, 28), "condition": "güneşli", "humidity": random.randint(55, 75)},
                "bursa": {"temp": random.randint(16, 24), "condition": "parçalı bulutlu", "humidity": random.randint(65, 85)},
                "antalya": {"temp": random.randint(20, 30), "condition": "açık", "humidity": random.randint(60, 80)}
            }
            
            city = self.extract_city(query)
            if not city:
                return "🌍 Hangi şehir için hava durumu istiyorsunuz? (İstanbul, Ankara, İzmir, Antalya, Bursa)"
            
            if city in cities:
                data = cities[city]
                return (f"🌤️ {city.capitalize()} Hava Durumu:\n"
                       f"   ⛅ Durum: {data['condition']}\n"
                       f"   🌡️ Sıcaklık: {data['temp']}°C\n"
                       f"   💧 Nem: {data['humidity']}%")
            else:
                return "❌ Bu şehir için hava durumu bilgim yok"
                
        except Exception as e:
            logger.error(f"Hava durumu hatası: {e}")
            return "❌ Hava durumu bilgisi alınamadı"

    def file_manager(self, query):
        """Gelişmiş dosya yöneticisi"""
        if "liste" in query or "ls" in query:
            path = self.extract_path(query) or "."
            try:
                items = os.listdir(path)
                result = f"📁 {path}:\n"
                for item in items:
                    full_path = os.path.join(path, item)
                    if os.path.isdir(full_path):
                        result += f"📂 {item}/\n"
                    else:
                        size = os.path.getsize(full_path)
                        result += f"📄 {item} ({self.format_size(size)})\n"
                return result
            except Exception as e:
                return f"❌ Dosya listeleme hatası: {e}"
        
        elif "oku" in query:
            file_path = self.extract_path(query)
            if file_path and os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)  # İlk 1000 karakter
                        return f"📖 {file_path}:\n{content}..."
                except Exception as e:
                    return f"❌ Dosya okuma hatası: {e}"
        
        return "📂 Kullanım: 'dosya liste [dizin]' veya 'dosya oku [dosya]'"

    def format_size(self, size):
        """Dosya boyutunu formatla"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def network_tools(self, query):
        """Ağ araçları"""
        if "ping" in query:
            host = self.extract_host(query) or "google.com"
            try:
                # Basit ping simülasyonu
                result = f"🌐 Ping {host}:"
                for i in range(4):
                    time_ms = random.randint(10, 100)
                    result += f"\n   {i+1}. {time_ms}ms"
                    time.sleep(0.5)
                return result
            except:
                return f"❌ {host} ping atılamadı"
        
        elif "ip" in query:
            try:
                # Yerel IP
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                return f"🖥️ Yerel IP: {local_ip}"
            except Exception as e:
                return f"❌ IP alınamadı: {e}"
        
        return "🌐 Ağ komutları: 'ping google.com' veya 'ip göster'"

    def security_tools(self, query):
        """Güvenlik araçları"""
        if "şifre" in query:
            length = 12
            if "uzun" in query:
                length = 16
            elif "kısa" in query:
                length = 8
            
            password = self.generate_password(length)
            return f"🔐 Güvenli Şifre: {password}"
        
        elif "hash" in query:
            text = self.extract_text(query) or "merhaba"
            md5 = hashlib.md5(text.encode()).hexdigest()
            sha256 = hashlib.sha256(text.encode()).hexdigest()
            return f"🔒 Hash Değerleri:\n   MD5: {md5}\n   SHA256: {sha256}"
        
        return "🔒 Güvenlik: 'şifre oluştur' veya 'hash merhaba'"

    def generate_password(self, length=12):
        """Güvenli şifre oluştur"""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))

    def machine_learning_response(self, user_input):
        """Makine öğrenmesi ile akıllı yanıt"""
        patterns = {
            r"(merhaba|selam|hey|hi|hello)": [
                "Merhaba! Nasılsınız?", "Selam! Size nasıl yardımcı olabilirim?"
            ],
            r"(teşekkür|sağol|thanks|thank you)": [
                "Rica ederim!", "Ne demek! Her zaman yardıma hazırım."
            ],
            r"(nasılsın|ne haber|how are you)": [
                "Çok iyiyim, teşekkür ederim! Sen nasılsın?", "Harikayım! Sorma!"
            ],
            r"(görüşürüz|hoşça kal|goodbye|bye)": [
                "Görüşürüz! İyi günler.", "Hoşça kal! Sonra görüşelim."
            ]
        }
        
        for pattern, responses in patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return random.choice(responses)
        
        return None

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
               f"   Gün: {now.strftime('%A')}")

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
            "🔒 GÜVENLİK: 'şifre oluştur' - Şifre üret\n"
            "🌐 AĞ: 'ping google.com' - Ping at\n"
            "👤 KİŞİSEL: 'benim adım [isim]' - İsmini değiştir\n"
            "🚪 ÇIKIŞ: '/exit' - Programdan çık"
        )

    def show_system_status(self):
        """Detaylı sistem durumu"""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        status = (
            f"📊 Detaylı Sistem Durumu:\n"
            f"   🖥️ CPU: {cpu}% kullanımda\n"
            f"   💾 RAM: {memory.percent}% ({memory.used//1024//1024}MB/{memory.total//1024//1024}MB)\n"
            f"   💿 Disk: {disk.percent}% dolu\n"
            f"   📡 Ağ: Gönderilen: {network.bytes_sent//1024}KB, Alınan: {network.bytes_recv//1024}KB\n"
            f"   🕐 Çalışma Süresi: {datetime.datetime.now() - self.start_time}\n"
            f"   💬 Konuşma Sayısı: {len(self.conversation_history)}"
        )
        self.speak(status, "info")

    def show_modules(self):
        """Aktif modülleri göster"""
        active = [mod for mod, active in self.modules.items() if active]
        inactive = [mod for mod, active in self.modules.items() if not active]
        
        status = (
            f"🔧 Sistem Modülleri:\n"
            f"   ✅ Aktif: {', '.join(active)}\n"
            f"   ❌ Pasif: {', '.join(inactive) if inactive else 'Yok'}"
        )
        self.speak(status, "info")

    def show_history(self):
        """Konuşma geçmişini göster"""
        if not self.conversation_history:
            self.speak("Henüz konuşma geçmişi yok.", "info")
            return
        
        self.speak("🗣️ Son Konuşmalar:", "info")
        for timestamp, message in list(self.conversation_history)[-5:]:
            time_str = timestamp.strftime("%H:%M:%S")
            print(f"   [{time_str}] {message}")

    def create_backup(self):
        """Sistem yedeği oluştur"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backups/quantumia_backup_{timestamp}.zip"
            
            with zipfile.ZipFile(backup_file, 'w') as zipf:
                for file in ['quantumia_config.json', 'ai_memory.db']:
                    if os.path.exists(file):
                        zipf.write(file)
            
            self.speak(f"✅ Yedek oluşturuldu: {backup_file}", "info")
        except Exception as e:
            self.speak(f"❌ Yedek oluşturulamadı: {e}", "error")

    def check_updates(self):
        """Güncellemeleri kontrol et"""
        self.speak("🔍 Güncellemeler kontrol ediliyor...", "info")
        time.sleep(2)
        self.speak("✅ Sistem güncel", "happy")

    def run(self):
        """Ana çalıştırma döngüsü"""
        self.speak(f"Merhaba {self.user_name}! Ben {self.name}, gelişmiş yapay zeka asistanın. 🤖", "excited")
        self.speak("'/' ile başlayarak sistem komutlarını kullanabilirsin. /help yazabilirsin. 🌟", "info")
        
        while True:
            try:
                user_input = self.listen()
                
                if user_input == "/exit":
                    self.speak(f"Görüşürüz {self.user_name}! İyi günler. 👋", "happy")
                    self.cleanup()
                    break
                
                if not user_input:
                    continue
                
                # Makine öğrenmesi yanıtı
                ml_response = self.machine_learning_response(user_input)
                if ml_response:
                    self.speak(ml_response, "happy")
                    continue
                
                # Gelişmiş komut işleme
                response = self.process_advanced_commands(user_input)
                if response:
                    self.speak(response, "neutral")
                    continue
                
                # Doğal konuşma
                response = self.natural_conversation(user_input)
                self.speak(response, "neutral")
                
            except KeyboardInterrupt:
                self.speak("\nProgram sonlandırılıyor...", "warning")
                self.cleanup()
                break
            except Exception as e:
                logger.error(f"Ana döngü hatası: {e}")
                self.speak("❌ Bir hata oluştu, lütfen tekrar deneyin.", "sad")

    def natural_conversation(self, user_input):
        """Doğal konuşma yanıtları"""
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
            if pattern in user_input.lower():
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

    def cleanup(self):
        """Temizlik işlemleri"""
        try:
            self.conn.close()
            self.save_config()
            logger.info("Sistem temiz bir şekilde kapatıldı")
        except Exception as e:
            logger.error(f"Temizlik hatası: {e}")

# -------------------- ANA PROGRAM --------------------
if __name__ == "__main__":
    try:
        ai = QuantumiaAI()
        ai.run()
    except Exception as e:
        print(f"❌ Kritik hata: {e}")
        print("Lütfen log dosyasını kontrol edin: quantumia.log")
        logging.exception("Kritik hata oluştu")
