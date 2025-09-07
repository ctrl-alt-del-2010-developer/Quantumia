#!/usr/bin/env python3

import random
import os


ascii="""
   ██████                                     █████                                ███
  ███░░░░███                                  ░░███                                ░░░
 ███    ░░███ █████ ████  ██████   ████████   ███████   █████ ████ █████████████   ████   ██████
░███     ░███░░███ ░███  ░░░░░███ ░░███░░███ ░░░███░   ░░███ ░███ ░░███░░███░░███ ░░███  ░░░░░███
░███   ██░███ ░███ ░███   ███████  ░███ ░███   ░███     ░███ ░███  ░███ ░███ ░███  ░███   ███████
░░███ ░░████  ░███ ░███  ███░░███  ░███ ░███   ░███ ███ ░███ ░███  ░███ ░███ ░███  ░███  ███░░███
 ░░░██████░██ ░░████████░░████████ ████ █████  ░░█████  ░░████████ █████░███ █████ █████░░████████
   ░░░░░░ ░░   ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░    ░░░░░    ░░░░░░░░ ░░░░░ ░░░ ░░░░░ ░░░░░  ░░░░░░░░
                                                                                                   """
os.system("clear")
print(ascii)

# Basit cevap veritabanı
responses = {
    "merhaba": ["Merhaba!", "Selam!", "Nasılsın?"],
    "hello": ["Hello!", "Hi!", "How Are you?"],
    "nasılsın": ["İyiyim, sen nasılsın?", "Harikayım!", "İdare ederim."],
    "how are you": ["I am good. how are you?", "I'm great!", "I can manage."],
    "hoşça kal": ["Görüşürüz!", "Hoşça kal!", "Bir dahaki sefere!"],
    "goodbye": ["See you later!","Goodbye!","Next time!"],
    "adın ne": ["Benim Adım Quantumia.","Benim Adım Quantumia. OrionixOS'in Yapay Zekasıyım."],
    "whats your name": ["My Name Is Quantumia","My Name Is Quantumia. I Am Artificial Intelligence In OrionixOS"],
    "bir ağ nasıl hacklenir": ["Maalesef Bunu Yapamam.","Bunu Yapamam. Çünkü Bu Politikalara Aykırı."],
    "how to hack a network": ["I Can't Do This. Because It's Against Policy.","I Can't Do This."],
}

def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Üzgünüm, bunu anlamadım."

def main():
    print("Quantumia'ya hoşgeldiniz! Çıkmak için 'çık' yazın.")
    while True:
        user_input = input("Sen: ")
        if user_input.lower() == "çık":
            print("Quantumia: Görüşürüz!")
            break
        response = get_response(user_input)
        print(f"Parade: {response}")

if __name__ == "__main__":
    main()
