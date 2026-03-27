import cloudscraper
from bs4 import BeautifulSoup
import os
import time

def speak(text):
    # Termux ko bulwane ki command
    os.system(f'termux-tts-speak "{text}"')

def check_live_results():
    scraper = cloudscraper.create_scraper()
    URL = "https://dpboss.boston/"
    
    # Hum pichle result ko yaad rakhenge taaki baar-bar na bole
    last_kalyan = ""

    print("🚀 Jarvis Voice Engine ON...")
    speak("Jarvis engine on. Scanning main markets.")

    while True:
        try:
            response = scraper.get(URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Kalyan ka result dhundna (Example logic)
            # Aapke pichle successful scraper ka logic yahan aayega
            current_result = "112-42-589" # Yeh sirf example hai
            
            if current_result != last_kalyan:
                msg = f"Attention Sachin Bhai! Kalyan new result is {current_result}"
                print(f"📢 {msg}")
                speak(msg)
                last_kalyan = current_result
                
                # Saath hi saath GitHub par backup bhi bhej dega
                os.system("python AutoGit.py") 
            
            # Har 5 minute mein check karega
            time.sleep(300) 

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    check_live_results()
