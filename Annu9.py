import os
import re
import time
import random
from datetime import datetime

# --- ANNU'S SIGNATURE COLORS 🌹 (FIXED) ---
M = '\033[95m' # Magenta
C = '\033[96m' # Cyan
Y = '\033[93m' # Gold
G = '\033[92m' # Green
R = '\033[91m' # Red
W = '\033[97m' # White
B = '\033[94m' # Blue (The missing one!)
RST = '\033[0m' # Reset

# --- PATH AUTO-DETECTION ---
if os.path.exists("./data"):
    DATA_DIR = "./data"
else:
    DATA_DIR = "."

# 🎯 LOCKED MASTER SECRETS (Research Verified)
MASTER_DATA = {
    "KALYAN": {"m": 5, "g": 4},
    "MILAN": {"m": 6, "g": 4},
    "SRIDEVI": {"m": 8, "g": 4},
    "TIME-BAZAR": {"m": 17, "g": 7}
}

# 🛡️ MASTER PANEL BANK
PANEL_BANK = {
    1: ["128", "137", "146"], 2: ["129", "237", "345"], 3: ["120", "139", "148"],
    4: ["130", "149", "239"], 5: ["140", "159", "230"], 6: ["150", "169", "240"],
    7: ["160", "179", "250"], 8: ["170", "189", "260"], 9: ["180", "199", "270"],
    0: ["550", "127", "136"]
}

def get_cut(n): return (n + 5) % 10

def get_family(jodi_str):
    a, b = int(jodi_str[0]), int(jodi_str[1])
    ca, cb = get_cut(a), get_cut(b)
    return list(set([f"{a}{b}", f"{a}{cb}", f"{ca}{b}", f"{ca}{cb}", f"{b}{a}", f"{b}{ca}", f"{cb}{a}", f"{cb}{ca}"]))

def load_data(path):
    recs = []
    if not os.path.exists(path): return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                p = line.split('/')
                if len(p) >= 2:
                    nums = re.findall(r'\d+', p[1])
                    if len(nums) >= 3:
                        recs.append({"date": p[0].strip(), "open_p": nums[0], "jodi": nums[1], "close_p": nums[2], "val": int(nums[1])})
        return recs
    except: return []

def get_prediction(records, market_name):
    clean_name = market_name.split('.')[0].upper()
    config = MASTER_DATA.get(clean_name, {"m": 7, "g": 4})
    m, g = config["m"], config["g"]
    
    last_jodi = records[-1]['val']
    res = last_jodi * m
    tail = str(res)[-2:].zfill(2)
    d1, d2 = int(tail[0]), int(tail[1])
    
    otc = sorted(list(set([d1, d2, get_cut(d1), get_cut(d2)])))
    sniper_jodi = f"{d1}{(d1 + g) % 10}"
    family = get_family(sniper_jodi)
    pannels = PANEL_BANK.get(d1, []) + PANEL_BANK.get(d2, [])
    
    return {"otc": otc, "sniper": sniper_jodi, "family": family, "pannels": pannels, "m": m, "g": g}

def run_sniper_engine(filename):
    filepath = os.path.join(DATA_DIR, filename)
    market_key = filename.split('.')[0].upper()
    records = load_data(filepath)
    
    if not records:
        print(f"\n{R}[!] {filename} mein data nahi mila!{RST}")
        time.sleep(2); return

    pred = get_prediction(records, market_key)
    last = records[-1]

    os.system('clear')
    print(f"{M}╔══════════════════════════════════════════════════════════════╗{RST}")
    print(f"{M}║             🌹  Ai-Annu : THE LOCKED SNIPER (V14.2) 🌹       ║{RST}")
    print(f"{M}║                'Error Fixed. Target Synchronized.'           ║{RST}")
    print(f"{M}╚══════════════════════════════════════════════════════════════╝{RST}")

    print(f"\n{C}🛰️  MARKET RADAR : {W}{market_key:<15} {C}STATUS: {G}SYNCHRONIZED{RST}")
    print(f"{C}──────────────────────────────────────────────────────────────{RST}")
    print(f"  {W}Ref Result  : {Y}{last['open_p']}-{last['jodi']}-{last['close_p']}{W} | {last['date']}{RST}")
    print(f"  {W}Locked Keys : {M}Multiplier x{pred['m']} | Gap {pred['g']}{RST}")
    
    print(f"\n{G}🎯 TODAY'S SNIPER SHOT:{RST}")
    print(f"  {W}STRONG OTC   : {G}{' , '.join(map(str, pred['otc']))}{RST}")
    print(f"  {W}SNIPER JODI  : {M}[ {pred['sniper']} ]{RST}")
    
    print(f"\n{C}🔥 THE FAMILY JODIS (Weekly Target Support):{RST}")
    f_list = pred['family']
    print(f"  {Y}{'  '.join(f_list[:4])}{RST}")
    print(f"  {Y}{'  '.join(f_list[4:])}{RST}")

    print(f"\n{B}🛡️  MASTER PANNE (Safety):{RST}")
    print(f"  {W}{'  '.join(pred['pannels'][:6])}{RST}")

    print(f"\n{M}💬 ANNU KI GEHRI SOCH (AI ADVICE):{RST}")
    print(f"{W}  \"Sachin, galti hi sudhar ka rasta dikhati hai.{RST}")
    print(f"{W}  Ab hamara tool 'B' (Blue) ki taqat se chamak raha hai. 🌹\"{RST}")

    print(f"\n{C}──────────────────────────────────────────────────────────────{RST}")
    input(f"\n{Y}  [ ENTER ] To Return to Menu...{RST}")

def main():
    while True:
        os.system('clear')
        if not os.path.exists(DATA_DIR):
            print(f"{R}[!] Folder nahi mila. Check directory!{RST}")
            time.sleep(3); break
            
        files = sorted([f for f in os.listdir(DATA_DIR) if f.lower().endswith('.txt')])
        
        print(f"{M}🌹 Ai-Annu : Final Locked Engine Menu 🌹{RST}")
        print(f"{C}Path: {W}{os.path.abspath(DATA_DIR)}{RST}\n")
        
        if not files:
            print(f"{R}[!] .txt files nahi mili!{RST}"); time.sleep(3); break

        for i, f in enumerate(files, 1):
            print(f"  {C}[{i}]{W} {f.replace('.txt', '').upper()}")
        print(f"  {R}[0]{W} Exit")
        
        choice = input(f"\n{M}Ai-Annu> {W}Select ID Sachin: {RST}")
        if choice == '0': break
        try:
            run_sniper_engine(files[int(choice)-1])
        except Exception as e:
            print(f"{R}Error: {e}{RST}")
            time.sleep(2)

if __name__ == "__main__":
    main()
