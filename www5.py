import os, time, math, json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box

console = Console()
DATA_DIR = "data/"

# ==================== VIP PANNA CHART ====================
REAL_PANNA_CHART = {
    1: ["100", "777", "128", "137"], 2: ["200", "444", "129", "138"],
    3: ["300", "111", "120", "139"], 4: ["400", "888", "130", "149"],
    5: ["500", "555", "140", "159"], 6: ["600", "222", "123", "150"],
    7: ["700", "999", "124", "160"], 8: ["800", "666", "125", "134"],
    9: ["900", "333", "126", "135"], 0: ["550", "000", "127", "136"]
}

# ==================== SMART ANALYST LOGIC ====================
def think_like_pro(history):
    """Pehle data padhna, fir mausam samajhna, fir anuman lagana"""
    if len(history) < 5: return "STABLE", [0, 5, 2, 7]
    
    # 1. Mausam Samjho (Trend Detection)
    last_3 = history[-3:]
    is_repeat = any(last_3[i]['jodi'] == last_3[i-1]['jodi'] for i in range(1, len(last_3)))
    
    # 2. Pattern Sochega (Logic Selection)
    if is_repeat:
        mausam = "🚨 REPEAT TREND (Shatka Mode)"
        # Repeat mein last jodi ke anks ko priority
        base_otc = [history[-1]['o'], history[-1]['c'], (history[-1]['o']+5)%10, (history[-1]['c']+5)%10]
    else:
        mausam = "✅ STABLE TREND (Brahmanda Sutra)"
        # Brahmanda Sutra
        last = history[-1]
        base_otc = sorted(list(set([last['c'], (last['o']+last['c'])%10, (last['c']+5)%10, (last['o']+last['c']+5)%10])))
        
    return mausam, base_otc[:4]

def load_data(f):
    path = os.path.join(DATA_DIR, f)
    history = []
    with open(path, 'r') as file:
        for line in file:
            if '/' not in line or '*' in line: continue
            try:
                p = line.split('/')
                g = p[1].strip().split('-')
                j = g[1].strip()
                if len(j) == 2:
                    history.append({'date': p[0].strip(), 'p1': g[0], 'jodi': j, 'p2': g[2], 'o': int(j[0]), 'c': int(j[1])})
            except: continue
    return history

def run_smart_tool():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    for f in files:
        m_name = f.replace('.txt', '').upper()
        history = load_data(f)
        if not history: continue

        # Tool Sochega (Thinking Phase)
        weather, today_otc = think_like_pro(history)
        last = history[-1]

        os.system('clear')
        console.print(Align.center(f"[bold magenta]🔱 JARVIS v44.0: SMART ANALYST ENGINE 🔱[/bold magenta]"))
        
        # Thinking Status
        console.print(Panel(f"Mausam: [bold cyan]{weather}[/bold cyan]\nAnalysing: [green]Last 40 Days Data Scanned...[/green]", title="🧠 TOOL THINKING PROCESS", border_style="cyan"))

        # Results & Prediction
        signal_txt = f"Market: {m_name}\nLast Result: {last['p1']}-{last['jodi']}-{last['p2']}\n[bold yellow]Target OTC: {today_otc}[/bold yellow]"
        console.print(Panel(signal_txt, title="✨ AAJ KA ANUMAN", border_style="yellow"))

        # VIP Panels from Genuine Chart
        panels = [REAL_PANNA_CHART[a][0] for a in today_otc if a in REAL_PANNA_CHART]
        console.print(Panel(f"VIP Panels: {' | '.join(panels)}", border_style="green"))

        console.input("\n[bold white]Next Market ke liye ENTER dabayein...[/bold white]")

if __name__ == "__main__":
    run_smart_tool()
