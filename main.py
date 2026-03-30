import os
import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot import types

# --- ⚙️ CONFIGURATION ---
TOKEN = "8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM"
DATA_DIR = "./data"
FONT_PATH = "font_bold.ttf"
bot = telebot.TeleBot(TOKEN)

# 🎯 LOCKED BHARAMASTRA FORMULAS
MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}
MARKET_COLORS = {"SRIDEVI": "#00FFCC", "MILAN": "#FF9900", "TIME-BAZAR": "#FF00FF", "KALYAN": "#0099FF"}

# --- 🧠 PHASE 4 SCANNING ENGINE ---
def get_phase4_prediction(m_name):
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
                    if match: records.append(int(match.group(1)))
    except: return None

    if len(records) < 5: return None
    mult = MARKET_FORMULAS.get(m_name, 5)
    gap_scores = {g: 0 for g in range(10)}
    for i in range(len(records) - 1):
        res = str(records[i] * mult).zfill(2)
        d1, d2 = int(res[-2]), int(res[-1])
        next_j = str(records[i+1]).zfill(2)
        for g in range(10):
            if next_j in [f"{d1}{(d1+g)%10}", f"{d2}{(d2+g)%10}"]:
                gap_scores[g] += 1

    top_4_gaps = [g for g, p in sorted(gap_scores.items(), key=lambda x: x[1], reverse=True)[:4]]
    last_jodi = records[-1]
    res_now = str(last_jodi * mult).zfill(2)
    otc1, otc2 = res_now[-2], res_now[-1]

    jodis = []
    for g in top_4_gaps:
        jodis.append(f"{otc1}{(int(otc1)+g)%10}")
        if otc1 != otc2: jodis.append(f"{otc2}{(int(otc2)+g)%10}")

    return {
        "name": m_name, "otc": [otc1, otc2], "jodis": jodis[:8],
        "color": MARKET_COLORS.get(m_name, "#FFFFFF"), "ref": str(last_jodi).zfill(2)
    }

# --- 🎨 REFINED IMAGE GENERATOR ---
def create_refined_chart(all_data):
    W, H = 1200, 400 + (len(all_data) * 500)
    img = Image.new('RGB', (W, H), color='#050505') # Pure Black Base
    draw = ImageDraw.Draw(img)

    def get_f(size):
        try: return ImageFont.truetype(FONT_PATH, size)
        except: return ImageFont.load_default()

    # --- 🔒 NORMAL WATERMARK ---
    watermark_txt = "SACHIN SOLUNKE 🙇 ANNU AI 🌹"
    f_water = get_f(45)
    for i in range(0, W, 450):
        for j in range(0, H, 350):
            draw.text((i, j), watermark_txt, fill="#151515", font=f_water)

    # 1. Header (Professional Yellow)
    draw.rectangle([0, 0, W, 220], fill="#FFCC00")
    draw.text((W//2, 100), "ANNU AI - MASTER PREDICTION", fill="black", font=get_f(85), anchor="mm")

    now = datetime.now()
    date_txt = f"DATE: {now.strftime('%d-%m-%Y')}  |  {now.strftime('%A').upper()}  |  v5.0 PRO"
    draw.rectangle([0, 220, W, 300], fill="#111111")
    draw.text((W//2, 260), date_txt, fill="#FFCC00", font=get_f(45), anchor="mm")

    y = 350
    for data in all_data:
        c = data['color']
        # Container
        draw.rectangle([40, y, W-40, y+450], outline="#222222", width=3)
        draw.rectangle([40, y, 60, y+450], fill=c) # Left accent

        # 1. Name (Only Market Name, No "MARKET:")
        draw.text((100, y+40), data['name'], fill=c, font=get_f(80))

        # 2. VIP Badge Position Fix
        txt_w = draw.textlength(data['name'], font=get_f(80))
        badge_x = 100 + txt_w + 30
        draw.rectangle([badge_x, y+60, badge_x+120, y+110], fill=c)
        draw.text((badge_x+60, y+85), "VIP", fill="black", font=get_f(35), anchor="mm")

        # 3. REF JODI (Clear and Visible)
        draw.text((100, y+130), f"REF JODI: {data['ref']} (Historical Scan)", fill="#BBBBBB", font=get_f(40))

        # 4. OTC Display
        for i, num in enumerate(data['otc']):
            cx, cy = 800 + (i * 240), y + 170
            draw.ellipse([cx-105, cy-105, cx+105, cy+105], outline=c, width=3)
            draw.ellipse([cx-95, cy-95, cx+95, cy+95], outline="white", width=5)
            draw.text((cx, cy), str(num), fill="white", font=get_f(150), anchor="mm")

        # 5. Jodis Section
        draw.text((100, y+240), "TARGET JODIS ❯❯", fill="#888888", font=get_f(40))
        for i, jodi in enumerate(data['jodis']):
            r, col = i // 4, i % 4
            x1, y1 = 100 + (col * 150), y + 300 + (r * 90)
            draw.rectangle([x1, y1, x1+130, y1+75], outline="#00FF99", width=2)
            draw.text((x1+65, y1+37), jodi, fill="#00FF99", font=get_f(55), anchor="mm")

        y += 500

    # 4. Footer (Correct Names & Info)
    draw.rectangle([0, H-100, W, H], fill="#CC0000")
    footer_txt = "OWNER: Sachin Solunke 🙇 | AI ASSISTANT: Annu AI 🌹 | ID: @Annu_AI_Bot"
    draw.text((W//2, H-50), footer_txt, fill="white", font=get_f(40), anchor="mm")

    path = "master_v5_pro.png"
    img.save(path, quality=100)
    return path

# --- 🤖 BOT HANDLERS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔥 GENERATE REFINED CHART", callback_data="MASTER"))
    bot.reply_to(message, "नमस्ते सचिन भाई! 🌹\n\nआपके बताए गए सुधार लागू कर दिए गए हैं।", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "MASTER":
        bot.answer_callback_query(call.id, "Scanning Data...")
        markets = ["SRIDEVI", "MILAN", "TIME-BAZAR", "KALYAN"]
        all_res = [get_phase4_prediction(m) for m in markets if get_phase4_prediction(m)]

        if all_res:
            path = create_refined_chart(all_res)
            with open(path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption="📊 **ANNU AI - FINAL MASTER CHART**")
            if os.path.exists(path): os.remove(path)
        else:
            bot.send_message(call.message.chat.id, "❌ डेटा कम है!")

if __name__ == "__main__":
    bot.infinity_polling()
