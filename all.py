import os
import re
import time
import requests
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- ⚙️ CONFIGURATION ---
BOT_TOKEN = "8733244182:AAHe3TQ-nYOYCrcjQnwzFZD4cZUTsU2q3sM"
CHAT_ID = "YOUR_CHAT_ID_HERE" 
DATA_DIR = "./data"
GITHUB_REPO_PATH = "."

# Panna Data
PANNA_DATA = {
    1: ["100", "777", "128", "137"], 2: ["200", "444", "129", "138"],
    3: ["300", "111", "120", "139"], 4: ["400", "888", "130", "149"],
    5: ["500", "555", "140", "159"], 6: ["600", "222", "123", "150"],
    7: ["700", "999", "124", "160"], 8: ["800", "666", "125", "134"],
    9: ["900", "333", "126", "135"], 0: ["550", "000", "127", "136"]
}

# --- 🧠 CORE ENGINE ---
def get_pro_results(filename):
    filepath = os.path.join(DATA_DIR, filename)
    m_name = filename.replace('.txt', '').upper()
    
    try:
        with open(filepath, 'r') as f:
            lines = [l for l in f if l.strip() and "***" not in l]
            last_jodi = int(re.search(r'- (\d{2}) -', lines[-1]).group(1))
    except: return None

    # Asli Bharamastra Formula
    mult = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}.get(m_name, 5)
    res = str(last_jodi * mult).zfill(2)
    otc1, otc2 = int(res[-2]), int(res[-1])
    
    # Top 4 Gap Patterns
    jodis = []
    for g in [0, 1, 5, 9]:
        jodis.append(f"{otc1}{(otc1+g)%10}")
        if otc1 != otc2: jodis.append(f"{otc2}{(otc2+g)%10}")
        
    return {"name": m_name, "otc": [otc1, otc2], "jodis": jodis[:8], "date": datetime.now().strftime("%d-%m-%Y")}

# --- 🖼️ VIP CARD GENERATOR ---
def create_vip_card(res_list):
    # Dynamic height based on number of markets
    img_h = 200 + (len(res_list) * 300)
    img = Image.new('RGB', (1000, img_h), color='#0a0a0a')
    draw = ImageDraw.Draw(img)
    
    # Gold Header
    draw.rectangle([0, 0, 1000, 150], fill="#FFD700")
    draw.text((200, 40), "S.A. VIP ALL MARKET CHART", fill="black")

    y = 180
    for r in res_list:
        # Market Box
        draw.rectangle([30, y, 970, y+270], outline="#FFD700", width=4)
        draw.text((60, y+20), f"MARKET: {r['name']} ({r['date']})", fill="#FFD700")
        
        # OTC & Panna
        p1 = " ".join(PANNA_DATA.get(r['otc'][0], [])[:3])
        p2 = " ".join(PANNA_DATA.get(r['otc'][1], [])[:3])
        draw.text((60, y+80), f"OTC: {r['otc'][0]}  |  {r['otc'][1]}", fill="white")
        draw.text((60, y+150), f"PANEL: {p1} | {p2}", fill="#00FF00")
        draw.text((60, y+210), f"JODIS: {'  '.join(r['jodis'])}", fill="white")
        y += 300

    path = "vip_all_market.png"
    img.save(path)
    return path

# --- 🐙 GITHUB & TELEGRAM SYNC ---
def sync_all(msg, img=None):
    # 1. Telegram Push
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    if img:
        with open(img, 'rb') as f:
            requests.post(url + "sendPhoto", data={'chat_id': CHAT_ID, 'caption': msg}, files={'photo': f})
    else:
        requests.post(url + "sendMessage", data={'chat_id': CHAT_ID, 'text': msg})
    
    # 2. GitHub Push
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-Update"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ GitHub & Telegram Synced!")
    except: print("⚠️ GitHub Sync Failed.")

# --- 📱 MAIN MENU ---
def main():
    while True:
        os.system('clear')
        print("🚀 ANNU-AI MASTER CONTROL (v17.0)")
        print("1. Scan & Send All (Auto-Mode)")
        print("2. Individual Market Scan")
        print("3. Manual GitHub Sync")
        print("4. Exit")
        
        opt = input("\nSelect: ")
        
        if opt == '1':
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            results = [get_pro_results(f) for f in files if get_pro_results(f)]
            card = create_vip_card(results)
            sync_all("📊 Aaj Ka VIP Summary Chart", card)
            input("\nDone! Press Enter...")
            
        elif opt == '4': break

if __name__ == "__main__":
    main()
