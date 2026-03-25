import os
import time
from datetime import datetime

def sync_to_github():
    # Screen clear karke status dikhayega
    print(f"\033[96m[!] GitHub Sync Process: {datetime.now().strftime('%H:%M:%S')}\033[0m")
    
    # 1. Saari nayi files ko add karna
    os.system("git add .")
    
    # 2. Commit message mein date/time daal dena
    commit_msg = f"Auto-Update: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    os.system(f'git commit -m "{commit_msg}"')
    
    # 3. GitHub par push karna
    print("\033[93m[*] Pushing latest updates to GitHub...\033[0m")
    result = os.system("git push origin main")
    
    if result == 0:
        print("\033[92m[✓] GitHub Synchronized Successfully!\033[0m")
    else:
        print("\033[91m[X] Sync Failed! Checking connection...\033[0m")

if __name__ == "__main__":
    print("\033[95m[SYSTEM] Sachin Bhai, Auto-Backup Engine ON hai! \033[0m")
    while True:
        sync_to_github()
        # 10 minute ka wait (600 seconds)
        time.sleep(600) 
