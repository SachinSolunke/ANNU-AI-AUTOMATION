import os
import re
import time
import requests
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- ⚙️ MASTER CONFIGURATION ---
BOT_TOKEN = "8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM"
CHAT_ID = "6190740924" # Maine aapka ID update kar diya hai
DATA_DIR = "./data"
GITHUB_REPO = "https://github.com/SachinSolunke/ANNU-AI-AUTOMATION.git"

# --- 🎨 HACKER THEME COLORS ---
G, Y, W, R, C, B = '\033[92m', '\033[93m', '\033[0m', '\033[91m', '\033[96m', '\033[94m'

# --- 🧠 VIP PANNA DATA ---
PANNA_MAP = {
    1: ["100", "777", "128", "137"], 2: ["200", "444", "129", "138"],
    3: ["300", "111", "120", "139"], 4: ["400", "888", "130", "149"],
    5: ["500", "555", "140", "159"], 6: ["600", "222", "123", "150"],
    7: ["700", "999", "124", "160"], 8: ["800", "666", "125", "134"],
    9: ["900", "333", "126", "135"], 0: ["550", "000", "127", "136"]
}

MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}

# --- 🚀 CORE LOGIC (BHARAMASTRA) ---
def get_hacker_results(filename):
    path = os.path.join(DATA_DIR, filename)
    m_name = filename.replace('.txt', '').upper()
    try:
        with open(path, 'r') as f:
            lines = [l.strip() for l in f if l.strip() and "***" not in l]
            last_jodi = int(re.search(r'- (\d{2}) -', lines[-1]).group(1))
    except: return None

    mult = MARKET_FORMULAS.get(m_name, 5)
    res = str(last_jodi * mult).zfill(2)
    otc1, otc2 = int(res[-2]), int(res[-1])
    
    # Advanced Gap Analysis
    jodis = [f"{otc1}{(otc1+g)%10}" for g in [0, 1, 5, 9]]
    if otc1 != otc2: jodis += [f"{otc2}{(otc2+g)%10}" for g in [0, 1, 5, 9]]
    
    return {"name": m_name, "otc": [otc1, otc2], "jodis": jodis[:8]}

# --- 🖼️ ADVANCED VIP CARD GENERATOR ---
def generate_hacker_card(results):
    h = 200 + (len(results) * 320)
    img = Image.new('RGB', (1100, h), color='#050505')
    draw = ImageDraw.Draw(img)
    
    # Header: Neon Hacker Style
    draw.rectangle([0, 0, 1100, 140], fill="#111111", outline="#00FF00", width=5)
    draw.text((280, 40), "ANNU AI - HACKER MOD VIP CHART", fill="#00FF00")

    y = 170
    for r in results:
        # Market Container
        draw.rectangle([40, y, 1060, y+290], outline="#00FF00", width=3)
        draw.text((70, y+20), f"SYS_SCAN: {r['name']} | DATE: {datetime.now().strftime('%d-%m-%Y')}", fill="#00FF00")
        
        # OTC Big Display
        draw.text((70, y+80), f"BASE_OTC: {r['otc'][0]}  :::  {r['otc'][1]}", fill="white")
        
        # Panna & Jodis
        p1 = " ".join(PANNA_MAP.get(r['otc'][0], [])[:3])
        p2 = " ".join(PANNA_MAP.get(r['otc'][1], [])[:3])
        draw.text((70, y+160), f"PANEL: {p1} | {p2}", fill="#FFFF00")
        draw.text((70, y+220), f"JODIS: {'  '.join(r['jodis'])}", fill="#00FFFF")
        y += 320

    path = "hacker_vip_report.png"
    img.save(path)
    return path

# --- 🛰️ SYNC ENGINE (TELEGRAM + GITHUB) ---
def sync_everything(img_path):
    print(f"{C}[*] Synchronizing System...{W}")
    
    # 1. Telegram Push
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(img_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': "🔥 ANNU AI PRO-SCAN COMPLETE!\nAll Markets Synced. 🌹"}, files={'photo': f})
        print(f"{G}[✔] Telegram Delivery Success!{W}")
    except: print(f"{R}[!] Telegram Offline.{W}")

    # 2. GitHub Push
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Hacker-Sync: {datetime.now().strftime('%H:%M')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"{G}[✔] GitHub Repositories Updated!{W}")
    except: print(f"{R}[!] GitHub Push Error.{W}")

# --- 📱 HACKER CONTROL MENU ---
def main():
    while True:
        os.system('clear')
        print(f"{G}┌──────────────────────────────────────────┐")
        print(f"│      💀 ANNU-AI HACKER TERMINAL v18.0    │")
        print(f"└──────────────────────────────────────────┘{W}")
        print(f"  {C}[1]{W} FULL SYSTEM SCAN (Auto-Mode)")
        print(f"  {C}[2]{W} MANUAL MARKET SCAN")
        print(f"  {C}[3]{W} GITHUB STATUS")
        print(f"  {R}[4]{W} SHUTDOWN SYSTEM")
        
        cmd = input(f"\n{G}ANNU@SACHIN_AI_~# {W}")

        if cmd == '1':
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            results = [get_hacker_results(f) for f in files if get_hacker_results(f)]
            if results:
                path = generate_hacker_card(results)
                sync_everything(path)
            input(f"\n{Y}System Synced. Press Enter to return...{W}")
        elif cmd == '4':
            print(f"{R}Logging out... Alvida Sachin Bhai! 🌹{W}")
            break

if __name__ == "__main__":
    main()
