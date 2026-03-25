import os
import re
import time
from datetime import datetime

# --- COLORS (Enhanced) ---
G = '\033[92m'  # Green (Pass)
Y = '\033[93m'  # Yellow (Warning)
W = '\033[0m'   # White
B = '\033[94m'  # Blue
R = '\033[91m'  # Red (Fail)
C = '\033[96m'  # Cyan
M = '\033[95m'  # Magenta
CY = '\033[1;36m' # Bold Cyan

DATA_DIR = "./data"

MARKET_CONF = {
    "MILAN": {"mult": 10, "pos": "TAIL"},
    "SRIDEVI": {"mult": 1, "pos": "HEAD"},
    "TIME-BAZAR": {"mult": 14, "pos": "TAIL"},
    "KALYAN": {"mult": 20, "pos": "HEAD"}
}

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    recs = []
    if not os.path.exists(path): return None
    try:
        with open(path, 'r') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) >= 2:
                    match = re.search(r'-\s*(\d{2})\s*-', parts[1])
                    if match:
                        val = int(match.group(1))
                        recs.append({'date': parts[0].strip()[:5], 'jodi': match.group(1), 'val': val})
    except: return None
    return recs

def get_otc(p1, p2, mult, pos):
    val = p1 * p2 * mult
    calc = str(val).zfill(4)
    target = calc[:2] if pos == "HEAD" else calc[-2:]
    d1, d2 = int(target[0]), int(target[1])
    return sorted(list(set([d1, d2, (d1+5)%10, (d2+5)%10])))

def get_market_accuracy(filename):
    data = load_data(filename)
    if not data or len(data) < 10: return 0
    m_name = filename.replace('.txt', '').upper()
    conf = MARKET_CONF.get(m_name, {"mult": 1, "pos": "HEAD"})
    pass_count = 0
    test_range = data[-10:]
    for i in range(len(test_range)):
        idx = (len(data) - len(test_range)) + i
        if idx < 2: continue
        curr = data[idx]
        p1, p2 = data[idx-1]['val'], data[idx-2]['val']
        otc = get_otc(p1, p2, conf['mult'], conf['pos'])
        if any(str(d) in curr['jodi'] for d in otc): pass_count += 1
    return (pass_count / len(test_range)) * 100

def main():
    while True:
        os.system('clear')
        now = datetime.now().strftime("%d-%m-%Y | %I:%M %p")
        
        # --- MAIN BANNER ---
        print(f"{M}╔{'═'*60}╗{W}")
        print(f"{M}║{CY}   ⚡ JARVIS v16.0 ULTRA MAXX ⚡   {M}║   {Y}{now}{W}")
        print(f"{M}╚{'═'*60}╝{W}")

        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        
        print(f"\n{B}┌{'─'*15}┬{'─'*25}┬{'─'*15}┐{W}")
        print(f"{B}│  ID  │      MARKET NAME        │  ACCURACY     │{W}")
        print(f"{B}├{'─'*15}┼{'─'*25}┼{'─'*15}┤{W}")

        for i, f in enumerate(files, 1):
            acc = get_market_accuracy(f)
            acc_color = G if acc >= 70 else (Y if acc >= 40 else R)
            m_display = f.replace('.txt', '').upper()
            print(f"{B}│ {W} [{i}]  {B}│{W} {m_display:<23} {B}│{acc_color}   {acc:>5.1f}%     {B}│{W}")
        
        print(f"{B}└{'─'*15}┴{'─'*25}┴{'─'*15}┘{W}")
        
        choice = input(f"\n{G}➤ Select Market (0 to Exit): {W}")
        if choice == '0': break
        
        try:
            filename = files[int(choice)-1]
            m_name = filename.replace('.txt', '').upper()
            data = load_data(filename)
            conf = MARKET_CONF.get(m_name, {"mult": 1, "pos": "HEAD"})
            
            os.system('clear')
            print(f"{M}◈ Market: {W}{m_name} | {Y}Loading Intelligence...{W}")

            # --- SUCCESS TRACKER TABLE ---
            print(f"\n{CY}╔{'═'*45}╗{W}")
            print(f"{CY}║       7-DAY PERFORMANCE TRACKER           ║{W}")
            print(f"{CY}╠{'═'*15}╦{'═'*12}╦{'═'*16}╣{W}")
            print(f"{CY}║    DATE     ║    JODI    ║     STATUS     ║{W}")
            print(f"{CY}╠{'═'*15}╬{'═'*12}╬{'═'*16}╣{W}")

            pass_count = 0
            recent_data = data[-7:]
            for i in range(len(recent_data)):
                idx = len(data) - len(recent_data) + i
                curr = data[idx]
                p1, p2 = data[idx-1]['val'], data[idx-2]['val']
                otc = get_otc(p1, p2, conf['mult'], conf['pos'])
                
                is_pass = any(str(d) in curr['jodi'] for d in otc)
                status = f"{G}PASS{W}" if is_pass else f"{R}FAIL{W}"
                if is_pass: pass_count += 1
                print(f"{CY}║{W}    {curr['date']}    {CY}║{W}    {curr['jodi']}    {CY}║{W}      {status:<12} {CY}║{W}")

            print(f"{CY}╚{'═'*15}╩{'═'*12}╩{'═'*16}╝{W}")

            # --- ACCURACY BOX ---
            prob = (pass_count / 7) * 100
            risk_color = G if prob >= 70 else (Y if prob >= 50 else R)
            print(f"\n{risk_color}▰▰▰ ACCURACY: {prob:.1f}% ▰▰▰{W}")
            
            # --- TODAY'S PREDICTION ---
            last_j, prev_j = data[-1]['val'], data[-2]['val']
            today_otc = get_otc(last_j, prev_j, conf['mult'], conf['pos'])
            avg_total = sum((d['val']//10 + d['val']%10)%10 for d in data[-3:]) // 3
            
            print(f"\n{M}💎 TODAY'S PREDICTION:{W}")
            print(f" {C}OTC: {G}{', '.join(map(str, today_otc))}{W}")
            
            generated_jodis = []
            for o in today_otc:
                partner = (avg_total - o) % 10
                generated_jodis.append(f"{o}{partner}")
                generated_jodis.append(f"{partner}{o}")

            print(f" {C}JODIS: {W}", end="")
            for j in list(set(generated_jodis))[:4]:
                print(f"{M}[{W}{j}{M}]{W}  ", end="")
            
            print(f"\n\n{G}──────────────────────────────────────────{W}")
            input(f"{G}Press [ENTER] to return to Main Menu{W}")
            
        except Exception as e:
            print(f"{R}Error: {e}{W}")
            time.sleep(2)
            continue

if __name__ == "__main__":
    main()
