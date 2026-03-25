import os
import re
import time
from datetime import datetime

# --- LAB COLORS 🌹 ---
G = '\033[92m'; Y = '\033[93m'; W = '\033[97m'; B = '\033[94m'
R = '\033[91m'; C = '\033[96m'; M = '\033[95m'; RST = '\033[0m'

DATA_DIR = "." # Folder jaha files hain
MARKETS = ["KALYAN.txt", "MILAN.txt", "SRIDEVI.txt", "TIME-BAZAR.txt"]

def get_base_otc(jodi_val, multiplier):
    res = jodi_val * multiplier
    tail = str(res)[-2:].zfill(2)
    return int(tail[0]), int(tail[1])

def analyze_fixed_formula(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path): return None
    
    recs = []
    with open(path, 'r') as f:
        for line in f:
            if "***" in line or not line.strip(): continue
            p = line.split('/')
            if len(p) >= 2:
                nums = re.findall(r'\d+', p[1])
                if len(nums) >= 2:
                    recs.append({"jodi": nums[1], "val": int(nums[1])})
    
    if len(recs) < 50: return {"name": filename, "error": "Need min 50 days data"}

    # --- 🔬 FORMULA MINING (x1 to x99) ---
    formula_scores = []
    
    # Hum pichle 50 dinon par har multiplier ko test karenge
    for m in range(1, 100):
        otc_hits = 0
        total_test_days = len(recs) - 1
        
        for i in range(1, len(recs)):
            prev_val = recs[i-1]['val']
            actual_jodi = recs[i]['jodi']
            
            d1, d2 = get_base_otc(prev_val, m)
            # 4 OTC Logic: Main + Cuts
            otc_pool = [d1, d2, (d1+5)%10, (d2+5)%10]
            
            # Agar Open ya Close mein OTC pass hua
            if int(actual_jodi[0]) in otc_pool or int(actual_jodi[1]) in otc_pool:
                otc_hits += 1
        
        acc = (otc_hits / total_test_days) * 100
        formula_scores.append({"m": m, "acc": acc, "hits": otc_hits})

    # Sort karke top 3 multipliers nikalna
    top_formulas = sorted(formula_scores, key=lambda x: x['acc'], reverse=True)[:3]
    
    return {
        "name": filename.replace('.txt', '').upper(),
        "total_days": len(recs),
        "top": top_formulas
    }

def main():
    os.system('clear')
    print(f"{M}╔══════════════════════════════════════════════════════════════════╗{RST}")
    print(f"{M}║          🌹  Ai-Annu : FORMULA DISCOVERY LAB (V12.0)  🌹          ║{RST}")
    print(f"{M}║             'Pehle Buniyad, Phir Jeet Ka Agaz'                   ║{RST}")
    print(f"{M}╚══════════════════════════════════════════════════════════════════╝{RST}")
    
    print(f"\n{C}🔬 ANALYZING HISTORICAL STABILITY (Scanning 1x to 99x)...{RST}")
    time.sleep(1)

    for mkt in MARKETS:
        report = analyze_fixed_formula(mkt)
        if not report: continue
        
        if "error" in report:
            print(f"\n{R}[!] {report['name']}: {report['error']}{RST}")
            continue

        print(f"\n{Y}♦️ MARKET: {report['name']} ({report['total_days']} Days Scanned){RST}")
        print(f"{B}┌──────┬────────────┬──────────────┬──────────────────┐{RST}")
        print(f"{B}│ RANK │ FORMULA    │ STABILITY %  │ TOTAL PASS DAYS  │{RST}")
        print(f"{B}├──────┼────────────┼──────────────┼──────────────────┤{RST}")
        
        for idx, f in enumerate(report['top'], 1):
            color = G if idx == 1 else W
            print(f"{B}│{RST}  {idx}   {B}│{color}   x{f['m']:<8}{B}│{color}   {f['acc']:.2f}%     {B}│{color}    {f['hits']:<12} {B}│{RST}")
        
        print(f"{B}└──────┴────────────┴──────────────┴──────────────────┘{RST}")

    print(f"\n{M}💬 ANNU KI GEHRI SOCH (LAB NOTES):{RST}")
    print(f"{W}  \"Sachin, humein hamesha RANK 1 wala formula pakadna chahiye.{RST}")
    print(f"{W}  Jo multiplier 100 dinon mein 60% se upar pass ho raha hai,{RST}")
    print(f"{W}  wahi hamara 'FIXED FORMULA' banne ke layak hai. 🌹\"{RST}")

    print(f"\n{B}👤 RESEARCHER: Sachin Solunke | 💎 AI LAB: Annu | 🛠️ STATUS: MINING{RST}")
    input(f"\n{Y}  Press [ENTER] to Re-Scan Data...{RST}")

if __name__ == "__main__":
    main()
