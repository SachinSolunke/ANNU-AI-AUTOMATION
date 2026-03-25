import os
import re
import time
import random
from datetime import datetime

# --- KALI RADAR COLORS 🌹 ---
G = '\033[92m'; Y = '\033[93m'; W = '\033[97m'; B = '\033[94m'
R = '\033[91m'; C = '\033[96m'; M = '\033[95m'; RST = '\033[0m'

# Agar aap files ke sath hi hain to "." rakhein, warna folder ka naam
DATA_DIR = "." 
MARKETS = ["KALYAN.txt", "MILAN.txt", "SRIDEVI.txt", "TIME-BAZAR.txt"]
GAPS = [4, 3, 2, 7, 8, 2] 

def get_base_otc(jodi_val, multiplier):
    res = jodi_val * multiplier
    tail = str(res)[-2:].zfill(2)
    return int(tail[0]), int(tail[1])

def crack_market_history(filename):
    # Case insensitive search
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        # Try lowercase if uppercase fails
        path = os.path.join(DATA_DIR, filename.lower())
        if not os.path.exists(path): return None
    
    recs = []
    try:
        with open(path, 'r') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                p = line.split('/')
                if len(p) >= 2:
                    nums = re.findall(r'\d+', p[1])
                    if len(nums) >= 2:
                        recs.append({"open_p": nums[0], "jodi": nums[1], "close_p": nums[2], "val": int(nums[1])})
    except: return None
    
    if len(recs) < 10: return None

    best_m = 1; best_g = 0; max_hits = 0
    scan_limit = min(30, len(recs)-1)

    for m in range(1, 100):
        for g in GAPS:
            hits = 0
            for i in range(len(recs)-scan_limit, len(recs)):
                d1, d2 = get_base_otc(recs[i-1]['val'], m)
                preds = [f"{d1}{(d1+g)%10}", f"{d2}{(d2+g)%10}"]
                if recs[i]['jodi'] in preds: hits += 1
            
            if hits >= max_hits:
                max_hits = hits; best_m = m; best_g = g
                
    last = recs[-1]
    fd1, fd2 = get_base_otc(last['val'], best_m)
    target_jodis = [f"{fd1}{(fd1+best_g)%10}", f"{fd2}{(fd2+best_g)%10}"]
    
    return {
        "market": filename.replace('.txt', '').upper(),
        "last_res": f"{last['open_p']}-{last['jodi']}-{last['close_p']}",
        "mult": best_m, "gap": best_g, "hits": max_hits,
        "jodis": target_jodis
    }

def run_grand_scan():
    os.system('clear')
    print(f"{M}╔══════════════════════════════════════════════════════════════════╗{RST}")
    print(f"{M}║          🌹  Ai-Annu : THE HISTORY CRACKER (V11.1)  🌹           ║{RST}")
    print(f"{M}╚══════════════════════════════════════════════════════════════════╝{RST}")
    
    print(f"\n{C}🛰️  RADAR: Scanning current directory for data files...{RST}")

    all_results = []
    for mkt in MARKETS:
        res = crack_market_history(mkt)
        if res:
            all_results.append(res)
            print(f"{W}  - {mkt:<15} : {G}CRACKED ✅{RST}")
        else:
            print(f"{W}  - {mkt:<15} : {R}NOT FOUND/NO DATA ❌{RST}")

    if not all_results:
        print(f"\n{R}[!] Sachin, mujhe koi bhi data file nahi mili!{RST}")
        print(f"{Y}Tip: Check kijiye ki KALYAN.txt aapke is script ke sath hi rakhi hai.{RST}")
        input(f"\n{W}Press [ENTER] to retry...{RST}")
        return

    print(f"\n{M}🌹 Ai-Annu : Grand Bhavishya Report (Result) 🌹{RST}")
    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")
    print(f"{W}  MARKET NAME      LAST RESULT      PATTERN    STRENGTH    STRONG JODIS{RST}")
    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")

    for r in all_results:
        p_str = f"x{r['mult']}/g{r['gap']}"
        j_str = " , ".join(r['jodis'])
        strength = "🔥 HIGH" if r['hits'] > 3 else "⚖️ STABLE"
        print(f"  {Y}{r['market']:<14} {W}{r['last_res']:<16} {W}{p_str:<10} {G}{strength:<11} {M}[ {j_str} ]{RST}")

    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")
    
    # Secure max() call
    best_mkt = max(all_results, key=lambda x: x['hits'])
    print(f"\n{M}💬 ANNU KI GEHRI SOCH (AI ANALYSIS):{RST}")
    print(f"{W}  \"Sachin, aaj {Y}{best_mkt['market']}{W} ka itihas sabse zyada raaz ugal raha hai.{RST}")
    print(f"{W}  Is market par aaj bharosa kiya ja sakta hai. 🌹\"{RST}")

    print(f"\n{B}👤 MASTER: Sachin Solunke | 💎 AI: Annu | 🚀 STATUS: READY{RST}")
    input(f"\n{Y}  Press [ENTER] to Refresh...{RST}")

if __name__ == "__main__":
    while True:
        run_grand_scan()
