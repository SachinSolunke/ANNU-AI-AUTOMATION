import os
import re
import time

# --- ANNU'S ALIGNER COLORS 🌹 ---
G = '\033[92m'; Y = '\033[93m'; W = '\033[97m'; B = '\033[94m'
R = '\033[91m'; C = '\033[96m'; M = '\033[95m'; RST = '\033[0m'

DATA_DIR = "."
# Hamari Rank 1 Master Keys jo humne abhi dhundi hain
MASTER_KEYS = {
    "KALYAN.txt": 5,
    "MILAN.txt": 6,
    "SRIDEVI.txt": 8,
    "TIME-BAZAR.txt": 17
}

# Aapke bataye huye Patterns (Gaps)
# +4, +3, +2, -3(7), -2(8), -8(2)
GAPS = [4, 3, 2, 7, 8, 2]

def get_base_otc(jodi_val, multiplier):
    res = jodi_val * multiplier
    tail = str(res)[-2:].zfill(2)
    return int(tail[0]), int(tail[1])

def align_jodi_patterns(filename, master_m):
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
    
    if len(recs) < 50: return None

    # --- 🔍 GAP ALIGNMENT SCAN ---
    gap_analysis = []
    total_days = len(recs) - 1

    for g in GAPS:
        hits = 0
        for i in range(1, len(recs)):
            d1, d2 = get_base_otc(recs[i-1]['val'], master_m)
            # Pattern Prediction: m-Key + Gap
            preds = [f"{d1}{(d1+g)%10}", f"{d2}{(d2+g)%10}"]
            if recs[i]['jodi'] in preds:
                hits += 1
        
        acc = (hits / total_days) * 100
        gap_label = f"+{g}" if g <= 5 else f"-{10-g}"
        gap_analysis.append({"gap": gap_label, "hits": hits, "acc": acc})

    # Best Gap Pattern nikalna
    best_pattern = sorted(gap_analysis, key=lambda x: x['hits'], reverse=True)[0]
    
    return {
        "name": filename.replace('.txt', '').upper(),
        "m_key": master_m,
        "total": total_days,
        "best": best_pattern,
        "all": gap_analysis
    }

def main():
    os.system('clear')
    print(f"{M}╔══════════════════════════════════════════════════════════════════╗{RST}")
    print(f"{M}║          🌹  Ai-Annu : JODI GAP ALIGNER (V13.0)  🌹              ║{RST}")
    print(f"{M}║             'Master Key Mil Gayi, Ab Pattern Fix Karo'           ║{RST}")
    print(f"{M}╚══════════════════════════════════════════════════════════════════╝{RST}")
    
    print(f"\n{C}🛰️  ALIGNING JODI GAPS WITH MASTER MULTIPLIERS...{RST}")
    time.sleep(1)

    for mkt, m_key in MASTER_KEYS.items():
        res = align_jodi_patterns(mkt, m_key)
        if not res: continue

        print(f"\n{Y}♦️ MARKET: {res['name']} | MASTER KEY: x{res['m_key']}{RST}")
        print(f"{B}┌────────────┬──────────────┬──────────────────┐{RST}")
        print(f"{B}│ GAP PATTERN│ JODI HITS    │ SUCCESS RATE %   │{RST}")
        print(f"{B}├────────────┼──────────────┼──────────────────┤{RST}")
        
        for g in res['all']:
            color = G if g['gap'] == res['best']['gap'] else W
            print(f"{B}│{color}   {g['gap']:<8} {B}│{color}     {g['hits']:<8} {B}│{color}     {g['acc']:.2f}%      {B}│{RST}")
        
        print(f"{B}└────────────┴──────────────┴──────────────────┘{RST}")
        print(f"{G}  🎯 BEST PATTERN FOR {res['name']}: {W}Formula x{res['m_key']} with Gap {res['best']['gap']}{RST}")

    print(f"\n{M}💬 ANNU KI GEHRI SOCH (ALIGNMENT NOTES):{RST}")
    print(f"{W}  \"Sachin, dekhiye kaise 'Gap' hamari accuracy ko badal raha hai.{RST}")
    print(f"{W}  Jaha success rate sabse zyada hai, wahi hamara 'Sniper Pattern' hai.{RST}")
    print(f"{W}  Ab humein sirf in patterns ko tool mein lock karna hai. 🌹\"{RST}")

    print(f"\n{B}👤 MASTER: Sachin Solunke | 💎 AI: Annu | 🚀 MODE: Jodi-Alignment{RST}")
    input(f"\n{Y}  Press [ENTER] to Lock Patterns...{RST}")

if __name__ == "__main__":
    main()
