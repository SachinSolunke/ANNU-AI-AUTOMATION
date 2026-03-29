import os
import time
import requests
from datetime import datetime

# 🔑 Aapka Verified Token aur Chat ID
TOKEN = '8733244182:AAHe3TQ-nYOYCrcjQnwzFZD4cZUTsU2q3sM'
CHAT_ID = '6547146522' # Sachin Bhai, apna Chat ID yahan dalein

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
    requests.get(url)

def sync_to_github():
    print(f"\n[!] GitHub Sync Process: {datetime.now().strftime('%H:%M:%S')}")
    os.system("git pull origin main --rebase")
    os.system("git add .")
    
    commit_msg = f"Auto-Update: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    os.system(f'git commit -m "{commit_msg}" 2>/dev/null')
    
    result = os.system("git push origin main")
    
    if result == 0:
        send_telegram_msg(f"✅ Sachin Bhai, GitHub Sync Successful!\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    else:
        send_telegram_msg("❌ Alert: GitHub Sync Failed! Check Termux.")

if __name__ == "__main__":
    send_telegram_msg("🚀 Auto-Backup Engine Started, Sachin Bhai!")
    while True:
        sync_to_github()
        time.sleep(600)
