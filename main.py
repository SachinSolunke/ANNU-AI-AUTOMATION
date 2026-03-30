
import os
import re
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot import types

# --- ⚙️ CONFIGURATION ---
TOKEN = "8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM"
DATA_DIR = "./data"
FONT_PATH = "font_bold.ttf"

# --- 🛠️ AUTO FONT SETUP ---
def setup_system_font():
    """Android System font ko local folder me copy karta hai font issue fix karne ke liye"""
    if not os.path.exists(FONT_PATH):
        # Android system fonts ke common locations
        paths = [
            "/system/fonts/NotoSerif-Bold.ttf",
            "/system/fonts/Roboto-Bold.ttf",
            "/system/fonts/DroidSans-Bold.ttf"
        ]
        found = False
        for p in paths:
            if os.path.exists(p):
                shutil.copy(p, FONT_PATH)
                print(f"✅ Font copied from: {p}")
                found = True
                break
        if not found:
            print("⚠️ Warning: System font nahi mila. Default font use hoga.")

setup_system_font()
bot = telebot.TeleBot(TOKEN)

# 🎯 Locked Formulas (Phase 4)
MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}

# --- 🧠 PHASE 4 PREDICTION ENGINE (TRUTH FINDER) ---
def get_full_prediction(m_name):
    filepath = os.path.join(DATA_DIR, f"{m_name}.txt")
    if not os.path.exists(filepath): return None

    records = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if "***" in line or not line.strip(): continue
                parts = line.split('/')
                if len(parts) >= 2:
                    match = re.search(r'-\s*(\d{2})\s*-', parts[1])
                    if match:
                        records.append(int(match.group(1)))
    except: return None

    if len(records) < 10: return None # Kam se kam 10 record scan ke liye

    mult = MARKET_FORMULAS.get(m_name, 5)
    gap_scores = {g: 0 for g in range(10)}

    # --- 🔍 SCANNING HISTORICAL GAPS (Truth Finder) ---
    for i in range(len(records) - 1):
        # Base OTC calculation
        res = str(records[i] * mult).zfill(2)
        d1, d2 = int(res[-2]), int(res[-1])
        
        tomorrow_jodi = str(records[i+1]).zfill(2)
        for g in range(10):
            j1 = f"{d1}{(d1 + g) % 10}"
            j2 = f"{d2}{(d2 + g) % 10}"
            if tomorrow_jodi == j1 or tomorrow_jodi == j2:
                gap_scores[g] += 1

    # Best 4 Gaps
    top_4_gaps = [g for g, _ in sorted(gap_scores.items(), key=lambda x: x[1], reverse=True)[:4]]

    # Today's Prediction
    last_jodi = records[-1]
    res_now = str(last_jodi * mult).zfill(2)
    otc1, otc2 = int(res_now[-2]), int(res_now[-1])

    jodis = []
    for g in top_4_gaps:
        jodis.append(f"{otc1}{(otc1 + g) % 10}")
        if otc1 != otc2:
            jodis.append(f"{otc2}{(otc2 + g) % 10}")

    return {
        "name": m_name, 
        "otc": [otc1, otc2], 
        "jodis": jodis[:8], 
        "ref": str(last_jodi).zfill(2)
    }

# --- 🎨 HD UI HELPER ---
def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    r = radius
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.ellipse([x1, y1, x1+2*r, y1+2*r], fill=fill)
    draw.ellipse([x2-2*r, y1, x2, y1+2*r], fill=fill)
    draw.ellipse([x1, y2-2*r, x1+2*r, y2], fill=fill)
    draw.ellipse([x2-2*r, y2-2*r, x2, y2], fill=fill)
    if outline:
        draw.line([x1+r, y1, x2-r, y1], fill=outline, width=width)
        draw.line([x1+r, y2, x2-r, y2], fill=outline, width=width)
        draw.line([x1, y1+r, x1, y2-r], fill=outline, width=width)
        draw.line([x2, y1+r, x2, y2-r], fill=outline, width=width)

# --- 🖼️ HD CHART GENERATOR ---
def create_master_chart(all_data):
    count = len(all_data)
    W, HEADER_H, DATE_H, CARD_H, CARD_GAP, FOOTER_H, PADDING = 1400, 260, 90, 420, 30, 110, 40
    H = HEADER_H + DATE_H + (CARD_H + CARD_GAP) * count + FOOTER_H + PADDING

    img = Image.new('RGB', (W, H), color='#080810')
    draw = ImageDraw.Draw(img)

    def get_f(size):
        try: return ImageFont.truetype(FONT_PATH, size)
        except: return ImageFont.load_default()

    # 🎨 1. HEADER (Gold Gradient Style)
    for i in range(HEADER_H):
        draw.line([(0, i), (W, i)], fill=(int(255-i/6), int(195-i/6), 0))
    draw.text((W//2, 110), "ANNU AI MASTER", fill='white', font=get_f(100), anchor='mm')
    draw.text((W//2, 200), "PHASE 4 - TRUTH FINDER PREDICTIONS", fill='#FFF8DC', font=get_f(45), anchor='mm')

    # 📅 2. DATE STRIP
    draw.rectangle([0, HEADER_H, W, HEADER_H+DATE_H], fill='#0D0D1F')
    now = datetime.now()
    date_str = f"DATE: {now.strftime('%d-%m-%Y')}   |   {now.strftime('%A').upper()}   |   v5.5 PRO"
    draw.text((W//2, HEADER_H+DATE_H//2), date_str, fill='#FFD700', font=get_f(48), anchor='mm')

    # 🃏 3. MARKET CARDS
    ACCENTS = ['#0066FF', '#FF6600', '#00BB44', '#CC00CC', '#FF2255']
    y = HEADER_H + DATE_H + 20

    for idx, data in enumerate(all_data):
        accent = ACCENTS[idx % len(ACCENTS)]
        cx1, cy1, cx2, cy2 = PADDING, y, W - PADDING, y + CARD_H
        
        # Card Background
        draw_rounded_rect(draw, [cx1, cy1, cx2, cy2], 24, fill='#11112A', outline='#1E1E44', width=2)
        draw.rectangle([cx1, cy1+24, cx1+10, cy2-24], fill=accent) # Left Color bar

        # Market Info
        draw.text((cx1+55, cy1+60), f"{data['name']}", fill=accent, font=get_f(70), anchor='lm')
        draw.text((cx1+55, cy1+130), f"REF JODI: {data['ref']} (Historical Scan)", fill='#777799', font=get_f(36), anchor='lm')

        # OTC Circles
        for i, num in enumerate(data['otc']):
            cx = W - PADDING - 100 - (1-i)*260
            draw.ellipse([cx-115, cy1+45, cx+115, cy1+275], fill=accent)
            draw.ellipse([cx-108, cy1+52, cx+108, cy1+268], fill='#1A1A85')
            draw.text((cx, cy1+160), str(num), fill='white', font=get_f(170), anchor='mm')

        # Target Jodis in Green Boxes
        draw.text((cx1+55, cy1+250), "TARGET JODIS >>", fill='#AAAAAA', font=get_f(40), anchor='lm')
        jx = cx1 + 55
        for jodi in data['jodis']:
            draw_rounded_rect(draw, [jx, cy1+290, jx+100, cy1+370], 12, fill='#091809', outline='#00FF55', width=2)
            draw.text((jx+50, cy1+330), jodi, fill='#00FF66', font=get_f(55), anchor='mm')
            jx += 115

        y += CARD_H + CARD_GAP

    # 🚩 4. FOOTER
    draw.rectangle([0, H-FOOTER_H, W, H], fill='#BB0000')
    draw.text((W//2, H-FOOTER_H//2), "OWNER: Sachin Solunke   |   POWERED BY: Annu AI 🌹", fill='white', font=get_f(42), anchor='mm')

    path = "master_chart.png"
    img.save(path, quality=100)
    return path

# --- 🤖 BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 SCAN ALL MARKETS (PHASE 4)", callback_data="MASTER"))
    bot.reply_to(message, "Namaste Sachin Bhai! 🌹\nPhase 4 Truth Finder System ready hai.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "MASTER":
        bot.answer_callback_query(call.id, "Scanning Historical Gaps...")
        files = [f.replace('.txt', '') for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
        all_res = [get_full_prediction(m) for m in files if get_full_prediction(m)]
        
        if all_res:
            bot.send_message(call.message.chat.id, "⏳ HD Chart taiyar ho raha hai...")
            path = create_master_chart(all_res)
            with open(path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=f"🎯 Phase 4 Master Chart (HD)\nMarkets Found: {len(all_res)}")
            if os.path.exists(path): os.remove(path)
        else:
            bot.send_message(call.message.chat.id, "❌ Data folder me scan ke liye पर्याप्त record nahi mile!")

if __name__ == "__main__":
    print("🚀 Annu AI Master Bot is Running...")
    bot.infinity_polling()
