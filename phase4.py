# START OF FILE phase3.py
import os
import re
import time

# --- HACKER COLORS ---
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
W = '\033[0m'   # White
B = '\033[94m'  # Blue
R = '\033[91m'  # Red
C = '\033[96m'  # Cyan
M = '\033[95m'  # Magenta

DATA_DIR = "./data"

# 🎯 LOCKED BHARAMASTRA FORMULAS (Jo humne Phase 1 se nikale the)
MARKET_FORMULAS = {
    "SRIDEVI": 8,
    "MILAN": 6,
    "TIME-BAZAR": 17,
    "KALYAN": 5
}

def load_clean_data(filepath):
    """File se sirf valid Jodis nikalta hai"""
    valid_records = []
    try:
        if not os.path.exists(filepath): return[]
        with open(filepath, 'r') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) >= 2:
                    date = parts[0].strip()
                    match = re.search(r'-\s*(\d{2})\s*-', parts[1])
                    if match:
                        jodi = match.group(1)
                        valid_records.append({"date": date, "jodi": jodi, "val": int(jodi)})
        return valid_records
    except: return[]

def get_base_otc(jodi_val, multiplier):
    """Locked formula se sirf 2 main Base OTC nikalta hai"""
    result = jodi_val * multiplier
    tail = str(result)[-2:].zfill(2)
    return int(tail[0]), int(tail[1])

def get_gap_label(gap):
    """Gap ko samajhne ke liye + ya - mein dikhata hai"""
    if gap == 0: return "SAME (0)"
    if gap <= 4: return f"+{gap} (Aage)"
    return f"-{10-gap} (Peeche)"

def analyze_jodi_patterns(filename):
    filepath = os.path.join(DATA_DIR, filename)
    market_name = filename.replace('.txt', '').upper()
    records = load_clean_data(filepath)
    
    if len(records) < 10:
        print(f"{R}[!] '{market_name}' ke liye data kam hai!{W}"); return

    # Market ka locked formula (Default 1 agar na mile)
    locked_mult = MARKET_FORMULAS.get(market_name, 1)

    # 10 tarah ke Gap ho sakte hain (0 se 9 tak)
    gap_scores = {g: 0 for g in range(10)}
    total_valid_days = len(records) - 1

    # --- SCANNING ENGINE (Sachai ka pata lagana) ---
    for i in range(total_valid_days):
        today = records[i]
        tomorrow = records[i+1]
        
        d1, d2 = get_base_otc(today['val'], locked_mult)
        
        # Har gap pattern ko check karenge
        for g in range(10):
            j1 = f"{d1}{(d1 + g) % 10}"
            j2 = f"{d2}{(d2 + g) % 10}"
            
            # Agar next day ki jodi humare gap formula se match hui
            if tomorrow['jodi'] == j1 or tomorrow['jodi'] == j2:
                gap_scores[g] += 1

    # Accuracy ke hisaab se Gaps ko sort karna
    sorted_gaps = sorted(gap_scores.items(), key=lambda x: x[1], reverse=True)
    
    os.system('clear')
    print(f"\n{M}╔══════════════════════════════════════════════════════════╗{W}")
    print(f"{M}║{W} {Y}🔍 JODI PATTERN SCANNER (TRUTH FINDER) : {market_name:<15}{W}{M}║{W}")
    print(f"{M}╚══════════════════════════════════════════════════════════╝{W}")
    print(f" {C}Locked Multiplier : {G}x{locked_mult}{W}")
    print(f" {C}Total Days Scanned: {G}{total_valid_days}{W}\n")

    print(f"{B}┌──────┬──────────────────────┬───────────┬──────────────┐{W}")
    print(f"{B}│{W} RANK {B}│{W} JODI PATTERN (GAP)   {B}│{W} PASS DAYS {B}│{W} ACCURACY %   {B}│{W}")
    print(f"{B}├──────┼──────────────────────┼───────────┼──────────────┤{W}")

    # Top 5 Best Gap Patterns dikhana
    top_4_gaps =[]
    for rank, (gap, passes) in enumerate(sorted_gaps[:5], 1):
        if passes == 0: continue
        acc = (passes / total_valid_days) * 100
        gap_label = get_gap_label(gap)
        if rank <= 4: top_4_gaps.append(gap) # Hum Top 4 gap nikalenge aaj ke liye
        
        color = G if rank <= 2 else Y
        print(f"{B}│{W}  {rank:<3} {B}│{W} {color}{gap_label:<20}{W} {B}│{W}    {passes:<6} {B}│{W}  {acc:.2f}%      {B}│{W}")
    
    print(f"{B}└──────┴──────────────────────┴───────────┴──────────────┘{W}")

    # --- AAJ KI JODIYAN (Sachai ke aadhar par) ---
    last_record = records[-1]
    td1, td2 = get_base_otc(last_record['val'], locked_mult)
    
    print(f"\n{Y}▶ AAJ KA SOLID GAME (Ref: {last_record['date']} | Jodi: {last_record['jodi']}){W}")
    print(f" {C}BASE OTC: {G}[ {td1}, {td2} ]{W}")
    
    print(f" {C}🔥 TARGET JODIS (Using Top 4 Historical Patterns):{W}")
    
    final_jodis =[]
    for g in top_4_gaps:
        final_jodis.append(f"{td1}{(td1 + g) % 10}")
        if td1 != td2: # Agar dono base digit same na ho
            final_jodis.append(f"{td2}{(td2 + g) % 10}")
            
    # Display the final Jodis
    jodi_str = "  ".join([f"{G}[{j}]{W}" for j in final_jodis])
    print(f"    {jodi_str}")

    print(f"\n{B}────────────────────────────────────────────────────────────{W}")
    input(f"{Y}Press [ENTER] to Scan Another Market...{W}")

def main():
    while True:
        os.system('clear')
        print(f"{G}============================================================{W}")
        print(f"{Y} 🤖 JARVIS JODI DISHA (DIRECTION) ENGINE (v3.5) 🤖{W}")
        print(f"{C}  'Hum dawa nahi karte, hum sirf sachai scan karte hain'{W}")
        print(f"{G}============================================================{W}")

        if not os.path.exists(DATA_DIR):
            print(f"{R}[!] 'data' folder nahi mila!{W}"); break

        files =[f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        if not files:
            print(f"{R}[!] Data folder empty hai!{W}"); break

        print(f"\n{C}Markets:{W}")
        for i, f in enumerate(files, 1):
            m_name = f.replace('.txt', '').upper()
            locked_f = MARKET_FORMULAS.get(m_name, "?")
            print(f"  {B}[{i}]{W} {m_name:<15} {G}[Locked Formula: x{locked_f}]{W}")
        print(f"  {R}[0]{W} EXIT SYSTEM")

        choice = input(f"\n{Y}JARVIS> Select Market Number: {W}")
        if choice == '0': break
        
        try:
            selected_file = files[int(choice)-1]
            analyze_jodi_patterns(selected_file)
        except (ValueError, IndexError):
            print(f"{R}[!] Invalid selection!{W}"); time.sleep(1)

if __name__ == "__main__":
    main()
