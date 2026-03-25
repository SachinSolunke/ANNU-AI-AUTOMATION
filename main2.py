#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, sys, re

# --- SNIPER THEME COLORS ---
G = '\033[92m'  # Green
Y = '\033[93m'  # Gold
W = '\033[97m'  # White
B = '\033[94m'  # Blue
R = '\033[91m'  # Red
C = '\033[96m'  # Cyan
P = '\033[95m'  # Purple
M = '\033[95m'  # Magenta (Added Fix)
RST = '\033[0m'

DATA_DIR = "./data"

# --- 1. DATA ENGINE ---
def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path): return None
    recs = []
    try:
        with open(path, 'r') as f:
            for line in f:
                if "**" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) < 2: continue
                date_str = parts[0].strip()
                nums = re.findall(r'\d+', parts[1])
                if len(nums) < 3: continue
                jodi = nums[1]
                if len(jodi) < 2: continue
                recs.append({
                    'date': date_str,
                    'jodi': int(jodi),
                    'open': int(jodi[0]),
                    'close': int(jodi[1]),
                    'total': (int(jodi[0]) + int(jodi[1])) % 10
                })
        return recs
    except: return None

# --- 2. OTC STRATEGY FINDER ---
def find_best_otc_strategy(records):
    scan_limit = 15
    if len(records) < scan_limit + 2: return None, 0
    scores = {}
    for m in range(1, 10): # 1=Direct, 2-9=Multipliers
        scores[f"x{m}_HEAD"] = 0; scores[f"x{m}_TAIL"] = 0

    start = len(records) - scan_limit
    for i in range(start, len(records)):
        curr = records[i]
        p1 = records[i-1]['jodi']; p2 = records[i-2]['jodi']

        # Helper to check Hit
        def check_hit(val, o, c):
            s_val = str(val).zfill(4)
            h_ank = [int(s_val[:2][0]), int(s_val[:2][1])]
            t_ank = [int(s_val[-2:][0]), int(s_val[-2:][1])]
            # Add cuts
            h_all = h_ank + [(x+5)%10 for x in h_ank]
            t_all = t_ank + [(x+5)%10 for x in t_ank]

            res_h = 1 if (o in h_all or c in h_all) else 0
            res_t = 1 if (o in t_all or c in t_all) else 0
            return res_h, res_t

        for m in range(1, 10):
            val = p1 * p2 * m
            h, t = check_hit(val, curr['open'], curr['close'])
            scores[f"x{m}_HEAD"] += h; scores[f"x{m}_TAIL"] += t

    best = max(scores, key=scores.get)
    return best, scores[best]

# --- 3. JODI PATTERN ANALYZER ---
def analyze_jodi_trends(records):
    totals = {}
    last_10 = records[-10:]
    for r in last_10:
        t = r['total']
        totals[t] = totals.get(t, 0) + 1
    # Get Top 3 Trending Totals
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:3]
    top_totals = [x[0] for x in sorted_totals]
    return top_totals

# --- 4. PANEL GENERATOR ---
def get_panels(ank):
    panels = {
        0: ["190", "280", "370", "460", "550"],
        1: ["128", "137", "146", "236", "245"],
        2: ["129", "237", "345", "480", "570"],
        3: ["120", "139", "148", "238", "580"],
        4: ["130", "149", "239", "338", "590"],
        5: ["140", "159", "230", "249", "339"],
        6: ["150", "169", "240", "349", "448"],
        7: ["160", "179", "250", "340", "449"],
        8: ["170", "260", "350", "440", "233"],
        9: ["180", "270", "360", "450", "117"]
    }
    return panels.get(ank, ["---"])

# --- 5. MAIN SYSTEM ---
def main():
    while True:
        os.system('clear')
        print(f"{P}╔{'═'*65}╗{RST}")
        print(f"{P}║   🎯 JARVIS v22.1 : SNIPER MODE (FIXED) 🎯          ║{RST}")
        print(f"{P}╚{'═'*65}╝{RST}")

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR); print(f"\n{R}[!] Data folder created.{RST}"); break
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not files: print(f"\n{R}[!] No Data Files.{RST}"); break

        print(f"\n{Y}  [+] SELECT TARGET MARKET:{RST}")
        for i, f in enumerate(files, 1):
            print(f"   {C}[{i}]{RST} {W}{f.replace('.txt', '')}{RST}")
        print(f"   {R}[0] EXIT{RST}")

        choice = input(f"\n{C}root@sniper:~# {RST}")
        if choice == '0': break

        try:
            filename = files[int(choice)-1]
            market_name = filename.replace('.txt', '').upper()
            data = load_data(filename)
            if not data or len(data) < 20:
                print(f"{R}[!] Need more data!{RST}"); time.sleep(2); continue

            print(f"\n{Y}🔄 CALCULATING FINAL SHOT FOR {market_name}...{RST}")

            # 1. Get Best OTC
            best_strat, score = find_best_otc_strategy(data)
            mult = int(re.findall(r'\d+', best_strat)[0])
            is_head = "HEAD" in best_strat

            # Predict Next OTC
            p1 = data[-1]['jodi']; p2 = data[-2]['jodi']
            val = p1 * p2 * mult
            s_val = str(val).zfill(4)
            targets = s_val[:2] if is_head else s_val[-2:]

            ank1, ank2 = int(targets[0]), int(targets[1])
            cut1, cut2 = (ank1+5)%10, (ank2+5)%10
            final_ank = sorted(list(set([ank1, ank2, cut1, cut2]))) # All 4 OTCs

            # 2. Get Trending Totals
            top_totals = analyze_jodi_trends(data)

            # 3. Build Jodis
            strong_jodis = []
            for ank in final_ank:
                for t in top_totals:
                    # Logic: If Open is 'ank', what Close makes Total 't'?
                    cl = (t - ank) % 10
                    # Highlight Main vs Cut
                    if ank in [ank1, ank2]:
                        strong_jodis.append(f"{G}{ank}{cl}{RST}") # Green for Main
                    else:
                        strong_jodis.append(f"{W}{ank}{cl}{RST}") # White for Support

            # 4. Build Panels (Only for Main 2 Anks)
            panels_1 = get_panels(ank1)
            panels_2 = get_panels(ank2)

            # --- DISPLAY ---
            os.system('clear')
            print(f"{G}╔{'═'*60}╗{RST}")
            print(f"{G}║  MARKET : {market_name:<15} |  STRATEGY : {best_strat:<10}   ║{RST}")
            print(f"{G}╚{'═'*60}╝{RST}")

            print(f"\n{Y}📊 TREND ANALYSIS:{RST}")
            print(f"   🔥 Trending Totals: {W}{top_totals}{RST} (Last 10 Days)")
            print(f"   💊 OTC Strength   : {W}{score}/15 Hits{RST}")

            print(f"\n{B}🎯 FINAL GAME PREDICTION:{RST}")
            print(f"{C}┌{'─'*60}┐{RST}")

            # OTC
            print(f"{C}│ {P}💎 STRONG OTC   : {W}[ {ank1} ]  [ {ank2} ] {Y}(Support: {cut1}, {cut2}){RST}".ljust(70) + f"{C}│{RST}")
            print(f"{C}├{'─'*60}┤{RST}")

            # JODI (Using comma separator for list)
            jodi_str = ", ".join(strong_jodis)
            # Truncate if too long to avoid breaking box
            if len(jodi_str) > 55: jodi_str = jodi_str[:55] + "..."

            print(f"{C}│ {M}🔫 SNIPER JODIS : {jodi_str}{RST}".ljust(70) + f"{C}│{RST}")
            print(f"{C}├{'─'*60}┤{RST}")

            # PANELS
            p_str1 = ", ".join(panels_1[:4])
            p_str2 = ", ".join(panels_2[:4])

            print(f"{C}│ {G}🛡️  PANELS ({ank1})  : {W}{p_str1}{RST}".ljust(70) + f"{C}│{RST}")
            print(f"{C}│ {G}🛡️  PANELS ({ank2})  : {W}{p_str2}{RST}".ljust(70) + f"{C}│{RST}")

            print(f"{C}└{'─'*60}┘{RST}")

            print(f"\n{R}⚠️ NOTE:{W} Green Jodis = Strong (Main OTC + Trend Total).{RST}")
            input(f"\n{W}[ PRESS ENTER ]{RST}")

        except Exception as e:
            print(f"Error: {e}"); input()

if __name__ == "__main__":
    main()

