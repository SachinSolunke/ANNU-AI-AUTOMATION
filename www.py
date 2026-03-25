#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════╗
║        🔱 PARAMAANU REAL TOOL - ACTUAL PREDICTIONS 🔱         ║
║     Hacker UI + Real Logic + Real Accuracy %                  ║
║                                                                ║
║  CREATOR: Sachin Solunke                                      ║
║  EMAIL: sachins8411@gmail.com | UPI: 8698431018-3@ibl         ║
║                                                                ║
║  ✅ REAL OTC | ✅ REAL ACCURACY | ✅ REAL LOGIC               ║
║  ✅ Date-Time | ✅ Pass/Fail History | ✅ Hacker Style UI     ║
╚════════════════════════════════════════════════════════════════╝
"""

import os, time, sys, json, sqlite3
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd
import numpy as np

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich import box
from rich.text import Text

console = Console()

# ============================================================================
# SETUP
# ============================================================================

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_DIR = os.path.join(BASE_DIR, 'database')

Path(DATA_DIR).mkdir(exist_ok=True)
Path(DB_DIR).mkdir(exist_ok=True)

CREATOR = {
    'name': 'Sachin Solunke',
    'email': 'sachins8411@gmail.com',
    'upi': '8698431018-3@ibl'
}

CUT_ANK = {0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4}

# ============================================================================
# HACKER STYLE ASCII ART
# ============================================================================

HEADER_ART = """
[bold cyan]
 █████╗ ██╗     ██████╗  █████╗ ██████╗  █████╗ ███╗   ███╗ █████╗ ███╗   ██╗██╗   ██╗
██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██╔══██║████╗ ████║██╔══██╗████╗  ██║██║   ██║
███████║██║     ██████╔╝███████║██████╔╝███████║██╔████╔██║███████║██╔██╗ ██║██║   ██║
██╔══██║██║     ██╔═══╝ ██╔══██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║
██║  ██║██║     ██║     ██║  ██║██║  ██║██║  ██║██║ ═╝ ██║██║  ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ [/bold cyan]
"""

# ============================================================================
# REAL DATA LOADER
# ============================================================================

def load_real_data(filepath):
    """Load actual market data"""
    try:
        if not os.path.exists(filepath):
            return None
        
        df = pd.read_csv(filepath, sep=r'\s*/\s*', header=None, engine='python',
                         names=['Date_Str', 'Pana_Jodi_Pana'])
        
        df = df.dropna(subset=['Pana_Jodi_Pana'])
        df = df[~df['Pana_Jodi_Pana'].str.contains(r"\*|x", na=False, case=False)]
        
        df[['Open_Pana', 'Jodi', 'Close_Pana']] = df['Pana_Jodi_Pana'].str.split(r'\s*-\s*', expand=True)
        
        for col in ['Open_Pana', 'Jodi', 'Close_Pana']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna().astype({'Open_Pana': int, 'Jodi': int, 'Close_Pana': int})
        
        df['open'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[0]))
        df['close'] = df['Jodi'].apply(lambda x: int(str(x).zfill(2)[1]))
        
        def parse_date(date_str):
            for fmt in ['%d-%m-%Y', '%d-%m-%y', '%m-%d-%Y', '%m-%d-%y']:
                try:
                    return pd.to_datetime(datetime.strptime(str(date_str).strip(), fmt))
                except:
                    pass
            return pd.NaT
        
        df['Date'] = df['Date_Str'].apply(parse_date)
        df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
        
        return df if len(df) > 0 else None
    except:
        return None

# ============================================================================
# REAL PREDICTION ENGINE
# ============================================================================

class RealPredictionEngine:
    """REAL algorithm - not fake!"""
    
    @staticmethod
    def calculate_real_otc(df):
        """Calculate REAL OTC from last record"""
        if len(df) < 1:
            return []
        
        last = df.iloc[-1]
        close_ank = last['close']
        cut_ank = CUT_ANK[close_ank]
        jodi_sum = (last['open'] + last['close']) % 10
        sum_cut = CUT_ANK[jodi_sum]
        
        otc = sorted(list(set([close_ank, cut_ank, jodi_sum, sum_cut])))
        return otc
    
    @staticmethod
    def calculate_real_accuracy(df):
        """Calculate REAL accuracy from historical data"""
        if len(df) < 5:
            return 0, 0, 0
        
        hits = 0
        total = 0
        
        # Last 40 days
        check_range = min(40, len(df) - 1)
        
        for i in range(1, check_range + 1):
            prev_record = df.iloc[-i-1]
            actual_record = df.iloc[-i]
            
            # Calculate prediction
            close_ank = prev_record['close']
            cut_ank = CUT_ANK[close_ank]
            jodi_sum = (prev_record['open'] + prev_record['close']) % 10
            sum_cut = CUT_ANK[jodi_sum]
            
            pred_otc = [close_ank, cut_ank, jodi_sum, sum_cut]
            
            # Check if hit
            if actual_record['open'] in pred_otc or actual_record['close'] in pred_otc:
                hits += 1
            
            total += 1
        
        accuracy = (hits / total * 100) if total > 0 else 0
        return accuracy, hits, total
    
    @staticmethod
    def get_pass_fail_history(df):
        """Get last 40 days pass/fail record"""
        records = []
        
        check_range = min(40, len(df) - 1)
        
        for i in range(1, check_range + 1):
            prev_record = df.iloc[-i-1]
            actual_record = df.iloc[-i]
            
            close_ank = prev_record['close']
            cut_ank = CUT_ANK[close_ank]
            jodi_sum = (prev_record['open'] + prev_record['close']) % 10
            sum_cut = CUT_ANK[jodi_sum]
            
            pred_otc = [close_ank, cut_ank, jodi_sum, sum_cut]
            
            is_pass = actual_record['open'] in pred_otc or actual_record['close'] in pred_otc
            
            records.append({
                'date': actual_record['Date'].strftime('%d-%m-%Y'),
                'day': actual_record['Date'].strftime('%a'),
                'jodi': str(actual_record['Jodi']).zfill(2),
                'open_pana': actual_record['Open_Pana'],
                'close_pana': actual_record['Close_Pana'],
                'pred_otc': ' '.join(map(str, pred_otc)),
                'status': '✅ PASS' if is_pass else '❌ FAIL'
            })
        
        return records

# ============================================================================
# HACKING ANIMATION
# ============================================================================

def hacking_animation(m_name):
    os.system('clear')
    console.print(Align.center(HEADER_ART))
    
    steps = [
        f"🔍 Locating {m_name} Server...",
        "💉 Injecting Quantum Logic...",
        "🔓 Cracking Weekly Radar...",
        "💎 Extracting Master Keys..."
    ]
    
    with console.status("[bold white]INITIALIZING REAL EXPLOIT...", spinner="aesthetic") as status:
        for step in steps:
            time.sleep(0.5)
            console.print(f"[bold green]OK[/bold green] {step}")
    time.sleep(0.5)

# ============================================================================
# REAL ENGINE DISPLAY
# ============================================================================

def real_engine(m_id, m_name, df):
    """Show REAL predictions with accuracy"""
    hacking_animation(m_name)
    
    if df is None or len(df) < 5:
        console.print("[bold red]❌ Insufficient data for this market[/bold red]")
        console.input("[white]Press ENTER...[/white]")
        return
    
    # Get REAL data
    otc = RealPredictionEngine.calculate_real_otc(df)
    accuracy, hits, total = RealPredictionEngine.calculate_real_accuracy(df)
    history = RealPredictionEngine.get_pass_fail_history(df)
    
    pred_date = pd.to_datetime(df.iloc[-1]['Date']) + timedelta(days=1)
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Display REAL OTC
    otc_text = ' , '.join(map(str, otc)) if otc else 'N/A'
    otc_panel = Panel(
        Align.center(f"[bold white]{otc_text}[/bold white]"),
        title="[bold cyan]REAL MASTER OTC[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE
    )
    
    # Display REAL accuracy
    acc_color = "green" if accuracy >= 70 else "yellow" if accuracy >= 50 else "red"
    accuracy_panel = Panel(
        Align.center(f"[bold {acc_color}]{accuracy:.2f}%[/bold {acc_color}]\n[dim]{hits}/{total} days passed[/dim]"),
        title="[bold magenta]REAL ACCURACY[/bold magenta]",
        border_style="magenta",
        box=box.DOUBLE
    )
    
    # Display Date-Time
    datetime_panel = Panel(
        Align.center(f"[bold yellow]{pred_date.strftime('%d-%m-%Y %A')}[/bold yellow]\n[dim]Time: {current_time}[/dim]"),
        title="[bold white]PREDICTION DATE[/bold white]",
        border_style="white",
        box=box.DOUBLE
    )
    
    console.print(Columns([otc_panel, accuracy_panel, datetime_panel]))
    
    # Show pass/fail history
    console.print("\n[bold cyan]📋 LAST 40 DAYS PASS/FAIL RECORD:[/bold cyan]\n")
    
    table = Table(border_style="cyan", show_header=True, header_style="bold cyan")
    table.add_column("Date", style="yellow")
    table.add_column("Day", style="white")
    table.add_column("Jodi", style="green")
    table.add_column("Prediction", style="blue")
    table.add_column("Status", justify="center")
    
    for record in history[:15]:  # Show last 15
        table.add_row(
            record['date'],
            record['day'],
            record['jodi'],
            record['pred_otc'],
            record['status']
        )
    
    console.print(table)
    console.print(f"\n[bold yellow]📊 Total: {total} days | Hits: {hits} | Accuracy: {accuracy:.2f}%[/bold yellow]")
    
    footer = Panel(
        Align.center(f"[bold green]✅ REAL SYSTEM VERIFIED[/bold green]\n[dim]Powered by Actual Market Data Analysis[/dim]"),
        title="✨ VERIFICATION STATUS",
        border_style="green"
    )
    console.print("\n" + str(footer))
    
    console.print("\n[bold blink yellow]>>> Press ENTER to Return to Command Center <<<[/bold blink yellow]")
    input()

# ============================================================================
# MARKET STATS - REAL DATA
# ============================================================================

def get_real_market_stats():
    """Get REAL stats from loaded data"""
    markets = [
        {"id": "1", "name": "KALYAN"},
        {"id": "2", "name": "MILAN"},
        {"id": "3", "name": "MILAN-NIGHT"},
        {"id": "4", "name": "SRIDEVI"},
        {"id": "5", "name": "SRIDEVI-NIGHT"},
        {"id": "6", "name": "TIME-BAZAR"},
    ]
    
    stats = []
    
    for market in markets:
        filepath = os.path.join(DATA_DIR, f"{market['name']}.txt")
        df = load_real_data(filepath)
        
        if df is None or len(df) < 5:
            accuracy = 0
            status = "❓ NO DATA"
            color = "white"
        else:
            accuracy, _, _ = RealPredictionEngine.calculate_real_accuracy(df)
            
            if accuracy >= 70:
                status = "🔥 HOT"
                color = "red"
            elif accuracy >= 50:
                status = "⚖️ STABLE"
                color = "yellow"
            else:
                status = "❄️ COLD"
                color = "blue"
        
        stats.append({
            'id': market['id'],
            'name': market['name'],
            'pass': f"{accuracy:.1f}%",
            'status': status,
            'color': color,
            'df': df
        })
    
    return stats

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def show_dashboard():
    """Main dashboard with REAL data"""
    while True:
        os.system('clear')
        console.print(Align.center(HEADER_ART))
        console.print(Align.center("[bold white]SYSTEM v28.0: REAL PREDICTION COMMAND CENTER[/bold white]\n"))
        
        stats = get_real_market_stats()
        
        table = Table(box=box.HORIZONTALS, header_style="bold magenta", expand=True, border_style="white")
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("MARKET NAME", style="bold white")
        table.add_column("WIN-RATE", justify="center")
        table.add_column("ALGORITHM STATUS", justify="center")
        
        for m in stats:
            table.add_row(m['id'], m['name'], f"[{m['color']}]{m['pass']}[/{m['color']}]", m['status'])
        
        console.print(table)
        
        now = datetime.now().strftime('%H:%M:%S')
        console.print(Panel(
            f"🛰️  [bold yellow]RADAR:[/bold yellow] ACTIVE  |  🕒 [bold yellow]TIME:[/bold yellow] {now}  |  "
            f"🚀 [bold yellow]ENGINE:[/bold yellow] REAL-DATA-V1  |  👤 [bold yellow]CREATOR:[/bold yellow] {CREATOR['name']}",
            border_style="cyan"
        ))
        
        choice = console.input("\n[bold cyan]root@gsm[/bold cyan]:[bold white]~[/bold white]# select_target -id: ")
        
        if choice == '0':
            break
        
        selected = next((m for m in stats if m['id'] == choice), None)
        if selected:
            real_engine(selected['id'], selected['name'], selected['df'])
        else:
            console.print("[bold red]ERROR: Invalid Target ID[/bold red]")
            time.sleep(1)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    try:
        show_dashboard()
    except KeyboardInterrupt:
        console.print("\n[bold cyan]👋 Goodbye...[/bold cyan]")
        sys.exit()
