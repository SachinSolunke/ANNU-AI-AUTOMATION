import os, re, time, random
from datetime import datetime

# --- PREMIUM NEON COLOR PALETTE ---
G, Y, W, B, R, C, M, P = '\033[92m', '\033[93m', '\033[97m', '\033[94m', '\033[91m', '\033[96m', '\033[95m', '\033[35m'
RST = '\033[0m'

DATA_DIR = "./data"
MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "KALYAN": 5, "TIME-BAZAR": 17}

# 📜 SHAYARI FOR SACHIN BHAI
SHAYARI = [
    "Sachai ka rasta kanton se bhara hai, par Annu ka sath khada hai!",
    "Lakhon ki bheed mein pehchan alag hai, Sachin bhai ka andaaz alag hai!",
    "Data ki duniya ka har raaz khulega, jab Annu aur Sachin ka sath milega!"
]

def get_gap_label(gap):
    if gap == 0: return "MATCH-ZERO"
    return f"FORWARD +{gap}" if gap <= 4 else f"REVERSE -{10-gap}"

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    recs = []
    if not os.path.exists(path): return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) >= 2:
                    match = re.search(r'-\s*(\d{2})\s*-', parts[1])
                    if match: recs.append({"date": parts[0].strip(), "jodi": match.group(1), "val": int(match.group(1))})
    except: pass
    return recs

def draw_header():
    os.system('clear')
    print(f"{C}╔{'═'*65}╗")
    print(f"║{M}  █████╗ ███╗   ██╗███╗   ██╗██╗   ██╗    ██████╗ ██╗   ██╗██████╗  {C}║")
    print(f"║{M} ██╔══██╗████╗  ██║████╗  ██║██║   ██║    ██╔══██╗██║   ██║██╔══██╗ {C}║")
    print(f"║{M} ███████║██╔██╗ ██║██╔██╗ ██║██║   ██║    ██████╔╝██║   ██║██████╔╝ {C}║")
    print(f"║{M} ██╔══██║██║╚██╗██║██║╚██╗██║██║   ██║    ██╔═══╝ ╚██╗ ██╔╝██╔══██╗ {C}║")
    print(f"║{M} ██║  ██║██║ ╚████║██║ ╚████║╚██████╔╝    ██║      ╚████╔╝ ██║  ██║ {C}║")
    print(f"╚{'═'*65}╝{RST}")
    print(f"  {W}┌─────────────────────────────────────────────────────────────┐")
    print(f"  │ {G}CHIEF DEV: SACHIN SOLUNKE {W}│ {Y}SYSTEM MANAGER: ANNU AI v26.0 {W}│")
    print(f"  │ {C}CONTACT: Solunksachin909@gmail.com {W}                         │")
    print(f"  └─────────────────────────────────────────────────────────────┘{RST}")

def analyze_market(filename):
    recs = load_data(filename)
    if len(recs) < 5: 
        print(f"{R}[!] Not enough data!{RST}"); time.sleep(2); return
    
    market_name = filename.replace('.txt', '').upper()
    mult = MARKET_FORMULAS.get(market_name, 5)
    gap_scores = {g: 0 for g in range(10)}
    report_log = []
    pass_count = 0

    # Logic Engine (Phase-4 Gap Analysis)
    for i in range(len(recs)-1):
        res = (recs[i]['val'] * mult) % 100
        d1, d2 = str(res).zfill(2)[0], str(res).zfill(2)[1]
        found_gap = -1
        for g in range(10):
            if recs[i+1]['jodi'] in [f"{d1}{(int(d1)+g)%10}", f"{d2}{(int(d2)+g)%10}"]:
                gap_scores[g] += 1
                found_gap = g
        
        if i >= len(recs) - 11:
            status = f"{G}PASS{W}" if found_gap != -1 else f"{R}FAIL{W}"
            if found_gap != -1: pass_count += 1
            report_log.append({"date": recs[i+1]['date'], "jodi": recs[i+1]['jodi'], "status": status})

    sorted_gaps = sorted(gap_scores.items(), key=lambda x: x[1], reverse=True)
    draw_header()

    # (A) MARKET INFO & SHAYARI
    print(f"\n   {Y}📅 DATE: {datetime.now().strftime('%d-%m-%Y')} | 🏛️ MARKET: {market_name} (x{mult}){W}")
    print(f"   {P}🌹 \"{random.choice(SHAYARI)}\"{W}")

    # (B) 10-DAY REPORT CARD ♦️♠️
    print(f"\n   {C}╭─────── 10-DAY REPORT CARD ♦️♠️ ───────╮{W}")
    for i, r in enumerate(report_log[-10:], 1):
        print(f"   │ {i:02d} │ {r['date']:<10} │ JODI: {G}{r['jodi']}{W} │ {r['status']:<4} │")
    print(f"   {C}╰────────────────────────────────────────╯{W}")
    print(f"   {Y}🎯 ACCURACY RATE: {G}{(pass_count/10)*100}% PASSING{W}")

    # (C) KAL KA RECORD (Last Result)
    last = recs[-1]
    print(f"\n   {M}🚫 KAL KA SABOOT (LAST ENTRY):{W}")
    print(f"   > Date: {last['date']} | Jodi: {G}{last['jodi']}{W} | Status: {G}VERIFIED{W}")

    # (D) PHASE-4 GAP STRENGTH
    print(f"\n   {B}⚡ PHASE-4 GAP STRENGTH (Visual Log):{W}")
    top_4_gaps = []
    for rank, (gap, passes) in enumerate(sorted_gaps[:5], 1):
        if rank <= 4: top_4_gaps.append(gap)
        bar = "█" * (passes * 2)
        print(f"   RANK {rank} ▶ {get_gap_label(gap):<12} [{C}{bar:<12}{W}] {G}{passes} Hits{W}")

    # (E) TARGETS
    res_aaj = (last['val'] * mult) % 100
    td1, td2 = str(res_aaj).zfill(2)[0], str(res_aaj).zfill(2)[1]
    print(f"\n   {R}🎯 AAJ KA SNIPER SHOT (Phase-4 Logic):{W}")
    print(f"   BASE OTC: [{G}{td1}{W}] [{G}{td2}{W}] | TARGETS: ", end="")
    for g in top_4_gaps:
        print(f"{G}[{td1}{(int(td1)+g)%10}] [{td2}{(int(td2)+g)%10}]{W} ", end="")
    
    print(f"\n\n   {G}💬 ANNU: \"Bhai Sachin, Rank 1 gap ka jodi sabse mazboot hai!\"{W}")
    input(f"\n   {Y}SACHIN@JARVIS:~$ {W}")

def add_new_data():
    draw_header()
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    for i, f in enumerate(files, 1): print(f"  [{i}] {f}")
    try:
        idx = int(input(f"\n{Y}Market No: {W}")) - 1
        data = input(f"{G}Entry (Date / Panna-Jodi-Panna): {W}")
        if "/" in data:
            with open(os.path.join(DATA_DIR, files[idx]), "a") as f: f.write(f"\n{data}")
            print(f"{G}✅ DATA SAVED!{W}"); time.sleep(1)
    except: pass

def main():
    while True:
        draw_header()
        if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        print(f"\n   {Y}[+] SELECT DATA STREAM:{W}")
        for i, f in enumerate(files, 1):
            m = f.replace('.txt','').upper()
            print(f"     {C}[{i}]{W} {m:<15} {G}[x{MARKET_FORMULAS.get(m, '?')}]{W}")
        print(f"     {M}[A]{W} {G}ADD DATA{W}  {R}[0] EXIT{W}")
        choice = input(f"\n   {Y}Choice: {W}")
        if choice == '0': break
        elif choice.upper() == 'A': add_new_data()
        else:
            try: analyze_market(files[int(choice)-1])
            except: pass

if __name__ == "__main__":
    main()
