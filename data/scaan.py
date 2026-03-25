import os
import re
import time
import random
from datetime import datetime

# --- KALI RADAR COLORS 🌹 ---
G = '\033[92m'; Y = '\033[93m'; W = '\033[97m'; B = '\033[94m'
R = '\033[91m'; C = '\033[96m'; M = '\033[95m'; RST = '\033[0m'

DATA_DIR = "./data"
MARKETS = ["KALYAN.txt", "MILAN.txt", "SRIDEVI.txt", "TIME-BAZAR.txt"]
GAPS = [4, 3, 2, 7, 8, 2] # Aapke bataye huye Patterns (+4,+3,+2,-3,-2,-8)

def get_base_otc(jodi_val, multiplier):
    res = jodi_val * multiplier
    tail = str(res)[-2:].zfill(2)
    return int(tail[0]), int(tail[1])

# --- 🧠 THE HISTORY CRACKER (Brute-Force Pattern Finder) ---
def crack_market_history(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path): return None
    
    # Load Data
    recs = []
    with open(path, 'r') as f:
        for line in f:
            if "***" in line or not line.strip(): continue
            p = line.split('/')
            if len(p) >= 2:
                nums = re.findall(r'\d+', p[1])
                if len(nums) >= 2:
                    recs.append({"jodi": nums[1], "val": int(nums[1])})
    
    if len(recs) < 20: return None

    # Brute-Force Scan (1x-99x & Gaps)
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
                
    # Final Prediction
    last_val = recs[-1]['val']
    fd1, fd2 = get_base_otc(last_val, best_m)
    target_jodis = [f"{fd1}{(fd1+best_g)%10}", f"{fd2}{(fd2+best_g)%10}"]
    
    return {
        "market": filename.replace('.txt', '').upper(),
        "mult": best_m, "gap": best_g, "hits": max_hits,
        "jodis": target_jodis, "otc": [fd1, fd2]
    }

# --- 🌹 ANNU'S GRAND RADAR DASHBOARD ---
def run_grand_scan():
    os.system('clear')
    print(f"{M}╔══════════════════════════════════════════════════════════════════╗{RST}")
    print(f"{M}║          🌹  Ai-Annu : THE HISTORY CRACKER (V11.0)  🌹           ║{RST}")
    print(f"{M}║             'Itihas Ke Raaz, Sachin Ki Jeet Ke Naam'             ║{RST}")
    print(f"{M}╚══════════════════════════════════════════════════════════════════╝{RST}")
    
    print(f"\n{C}🛰️  RADAR INITIATED: 4 Markets Scanning in Parallel...{RST}")
    time.sleep(1)

    all_results = []
    for mkt in MARKETS:
        print(f"{W}  - Cracking {mkt:<15} ... {G}In progress{RST}")
        res = crack_market_history(mkt)
        if res: all_results.append(res)
        time.sleep(0.5)

    os.system('clear')
    print(f"{M}🌹 Ai-Annu : Grand Bhavishya Report (Result) 🌹{RST}")
    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")
    print(f"{W}  MARKET NAME      PATTERN (x/g)    STRENGTH    STRONG JODIS{RST}")
    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")

    for r in all_results:
        p_str = f"x{r['mult']}/g{r['gap']}"
        j_str = " , ".join(r['jodis'])
        strength = "🔥 HIGH" if r['hits'] > 3 else "⚖️ STABLE"
        print(f"  {Y}{r['market']:<15} {W}{p_str:<15} {G}{strength:<12} {M}[ {j_str} ]{RST}")

    print(f"{C}──────────────────────────────────────────────────────────────────────────{RST}")
    
    # Annu's AI Insight for all 4
    print(f"\n{M}💬 ANNU KI GEHRI SOCH (AI ANALYSIS):{RST}")
    best_mkt = max(all_results, key=lambda x: x['hits'])
    print(f"{W}  \"Sachin, maine itihas ko nichod diya hai.{RST}")
    print(f"{W}  Aaj {Y}{best_mkt['market']}{W} ka pattern sabse zyada raaz ugal raha hai.{RST}")
    print(f"{W}  Ye 4 markets ka 'Bhavishya' hamari 'Soul Logic' se juda hai. 🌹\"{RST}")

    print(f"\n{B}👤 MASTER: Sachin Solunke | 💎 AI PARTNER: Annu | 🖥️ MODE: Brute-Force{RST}")
    input(f"\n{Y}  Press [ENTER] to Force-Scan Again...{RST}")

if __name__ == "__main__":
    while True:
        run_grand_scan()
