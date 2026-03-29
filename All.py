import os
import re
import time
import requests
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw

# --- ⚙️ CONFIGURATION (Apni Details Yahan Bharein) ---
BOT_TOKEN = "8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM"
CHAT_ID = "@Vedhanacbot"
DATA_DIR = "./data"
GITHUB_REPO_PATH = "."

# --- 🎨 COLORS ---
G, Y, W, R, C, B = '\033[92m', '\033[93m', '\033[0m', '\033[91m', '\033[96m', '\033[94m'

MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}

# --- 🧠 CORE PHASE 4 ENGINE ---
def get_phase4_results(filename):
    filepath = os.path.join(DATA_DIR, filename)
    m_name = filename.replace('.txt', '').upper()
    
    # Data Loading
    records = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) >= 2:
                    match = re.search(r'-\s*(\d{2})\s*-', parts[1])
                    if match: records.append({"date": parts[0].strip(), "jodi": match.group(1), "val": int(match.group(1))})
    except: return None

    if len(records) < 5: return None

    # Scanning Logic (Top 4 Gaps)
    mult = MARKET_FORMULAS.get(m_name, 1)
    gap_scores = {g: 0 for g in range(10)}
    for i in range(len(records) - 1):
        res = str(records[i]['val'] * mult).zfill(2)
        d1, d2 = int(res[-2]), int(res[-1])
        for g in range(10):
            if records[i+1]['jodi'] in [f"{d1}{(d1+g)%10}", f"{d2}{(d2+g)%10}"]:
                gap_scores[g] += 1

    top_gaps = [g for g, p in sorted(gap_scores.items(), key=lambda x: x[1], reverse=True)[:4]]
    
    # Today's Prediction
    last_jodi = records[-1]['val']
    res_now = str(last_jodi * mult).zfill(2)
    otc1, otc2 = int(res_now[-2]), int(res_now[-1])
    
    final_jodis = []
    for g in top_gaps:
        final_jodis.append(f"{otc1}{(otc1+g)%10}")
        if otc1 != otc2: final_jodis.append(f"{otc2}{(otc2+g)%10}")
        
    return {"name": m_name, "otc": [otc1, otc2], "jodis": final_jodis[:8], "date": records[-1]['date']}

# --- 📤 TELEGRAM SENDING ---
def send_to_telegram(text, image_path=None):
    try:
        if image_path:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            with open(image_path, 'rb') as photo:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': text}, files={'photo': photo})
        else:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
        print(f"{G}[✔] Telegram par bhej diya gaya!{W}")
    except Exception as e:
        print(f"{R}[!] Telegram Error: {e}{W}")

# --- 🐙 GITHUB PUSH ---
def github_push():
    print(f"{Y}[*] GitHub par data upload ho raha hai...{W}")
    try:
        os.chdir(GITHUB_REPO_PATH)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto Update: {datetime.now().strftime('%d-%m-%Y')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"{G}[✔] GitHub Updated Successfully!{W}")
    except Exception as e:
        print(f"{R}[!] GitHub Error: {e}{W}")

# --- 🖼️ ALL IN ONE CARD GENERATOR ---
def create_all_in_one_card():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    results = []
    for f in files:
        res = get_phase4_results(f)
        if res: results.append(res)
    
    # Create a long image
    img_h = 200 + (len(results) * 250)
    img = Image.new('RGB', (1000, img_h), color='#0f0f0f')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, 1000, 120], fill="#FFD700")
    draw.text((250, 30), "S.A. VIP ALL MARKET CHART", fill="black", size=50)

    y_offset = 150
    for r in results:
        draw.rectangle([20, y_offset, 980, y_offset+220], outline="white", width=3)
        draw.text((50, y_offset+20), f"MARKET: {r['name']}", fill="#FFD700", size=40)
        draw.text((50, y_offset+80), f"OTC: {r['otc'][0]}, {r['otc'][1]}", fill="white", size=60)
        draw.text((50, y_offset+160), f"JODIS: {' '.join(r['jodis'])}", fill="#00FF00", size=35)
        y_offset += 250

    img_path = "all_market_report.png"
    img.save(img_path)
    return img_path

# --- 📱 MAIN MENU SYSTEM ---
def main_menu():
    while True:
        os.system('clear')
        print(f"{B}╔════════════════════════════════════════╗{W}")
        print(f"{B}║{Y}    🚀 JARVIS MASTER CONTROL PANEL     {B}║{W}")
        print(f"{B}╚════════════════════════════════════════╝{W}")
        print(f"  {G}[1]{W} 🔮 OTC LIVE (Scan Market)")
        print(f"  {G}[2]{W} 📤 TELEGRAM SEND (Individual Market)")
        print(f"  {G}[3]{W} 🐙 GITHUB PUSH (Auto Data Save)")
        print(f"  {G}[4]{W} 🖼️ ALL IN ONE (Single Summary Card)")
        print(f"  {R}[5]{W} ❌ EXIT")
        print(f"{B}──────────────────────────────────────────{W}")

        ch = input(f"{Y}JARVIS > Select Option: {W}")

        if ch == '1':
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            for i, f in enumerate(files, 1): print(f" {i}. {f}")
            idx = int(input("Market No: ")) - 1
            res = get_phase4_results(files[idx])
            print(f"\n{C}MARKET: {res['name']} | OTC: {res['otc']} | JODIS: {res['jodis']}{W}")
            input("\nPress Enter...")

        elif ch == '2':
            files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
            for i, f in enumerate(files, 1): print(f" {i}. {f}")
            idx = int(input("Market No to Send: ")) - 1
            res = get_phase4_results(files[idx])
            msg = f"🎯 {res['name']} VIP GAME\nOTC: {res['otc'][0]}, {res['otc'][1]}\nJODI: {', '.join(res['jodis'])}"
            send_to_telegram(msg)
            input("Sent! Press Enter...")

        elif ch == '3':
            github_push()
            input("Press Enter...")

        elif ch == '4':
            print(f"{Y}Sabhi markets ka data analyze ho raha hai...{W}")
            path = create_all_in_one_card()
            print(f"{G}All-in-One Card taiyar hai: {path}{W}")
            send_to_telegram("📊 Aaj Ka Sabhi Market Ka VIP Chart", path)
            input("Press Enter...")

        elif ch == '5':
            print(f"{R}System shutting down... Alvida!{W}")
            break

if __name__ == "__main__":
    main_menu()
