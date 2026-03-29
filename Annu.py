import os
import re
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- CONFIG & COLORS ---
DATA_DIR = "./data"
G, Y, W, R = '\033[92m', '\033[93m', '\033[0m', '\033[91m'

# Aapke provide kiye gaye Panna
PANNA_DATA = {
    1: ["100", "777", "128", "137", "146", "236", "245", "290", "380", "470", "489", "560", "678", "579", "119", "155", "227", "335", "344", "399", "588", "669"],
    2: ["200", "444", "129", "138", "147", "156", "237", "246", "345", "390", "480", "570", "679", "589", "110", "228", "255", "336", "499", "660", "688", "778"],
    3: ["300", "111", "120", "139", "148", "157", "238", "247", "256", "346", "490", "580", "670", "689", "166", "229", "337", "355", "445", "599", "779", "788"],
    4: ["400", "888", "130", "149", "158", "167", "239", "248", "257", "347", "356", "590", "680", "789", "112", "220", "266", "338", "446", "455", "699", "770"],
    5: ["500", "555", "140", "159", "168", "230", "249", "258", "267", "348", "357", "456", "690", "780", "113", "122", "177", "339", "366", "447", "799", "889"],
    6: ["600", "222", "123", "150", "169", "178", "240", "259", "268", "349", "358", "457", "367", "790", "114", "277", "330", "448", "466", "556", "880", "899"],
    7: ["700", "999", "124", "160", "179", "250", "269", "278", "340", "359", "368", "458", "467", "890", "115", "133", "188", "223", "377", "449", "557", "566"],
    8: ["800", "666", "125", "134", "170", "189", "260", "279", "350", "369", "378", "459", "567", "468", "116", "224", "233", "288", "440", "477", "558", "990"],
    9: ["900", "333", "126", "135", "180", "234", "270", "289", "360", "379", "450", "469", "117", "478", "568", "144", "199", "225", "388", "559", "577", "667"],
    0: ["550", "000", "127", "136", "190", "235", "280", "279", "370", "479", "460", "569", "118", "578", "668", "244", "299", "226", "488", "550", "677", "389"]
}

MARKET_FORMULAS = {"SRIDEVI": 8, "MILAN": 6, "TIME-BAZAR": 17, "KALYAN": 5}

def generate_pro_card(m_name, otc1, otc2, jodis):
    now = datetime.now()
    img = Image.new('RGB', (800, 600), color='black')
    draw = ImageDraw.Draw(img)
    
    # Design elements
    draw.rectangle([0, 0, 800, 100], fill="#f2ea00") # Yellow Header
    draw.text((150, 30), f"LUCKY ANK CHART - {m_name}", fill="black")
    
    # Date/Day
    info_text = f"📅 {now.strftime('%d-%m-%Y')} | {now.strftime('%A')}"
    draw.text((30, 110), info_text, fill="white")
    
    # OTC Circles
    for x, val in [(150, otc1), (470, otc2)]:
        draw.ellipse([x, 150, x+180, 330], fill="#2b0057", outline="white", width=4)
        draw.text((x+60, 190), str(val), fill="white")

    # Jodis & Pannels
    p1 = " ".join(PANNA_DATA.get(otc1, [])[:4])
    p2 = " ".join(PANNA_DATA.get(otc2, [])[:4])
    draw.text((50, 350), f"PANEL: {p1} | {p2}", fill="#f2ea00")
    draw.text((50, 420), "🔥 TARGET JODIS:", fill="#92f22e")
    draw.text((50, 470), "  ".join(jodis), fill="white")
    
    # Permanent ID
    draw.rectangle([0, 550, 800, 600], fill="#0088cc")
    draw.text((250, 560), "JOIN: @Sachin_Annu_AI_Bot", fill="white")
    
    path = f"{DATA_DIR}/{m_name}_pro.png"
    img.save(path)
    return path

def analyze_jodi_patterns(filename, bot_mode=False):
    filepath = os.path.join(DATA_DIR, filename)
    m_name = filename.replace('.txt', '').upper()
    
    # Basic logic from phase4
    if not os.path.exists(filepath): return None, "No File"
    
    with open(filepath, 'r') as f:
        lines = [l for l in f if l.strip() and "***" not in l]
        last_jodi = int(re.search(r'- (\d{2}) -', lines[-1]).group(1))

    mult = MARKET_FORMULAS.get(m_name, 5)
    res = str(last_jodi * mult).zfill(2)
    otc1, otc2 = int(res[-2]), int(res[-1])
    
    jodis = [f"{otc1}{(otc1+g)%10}" for g in range(4)] + [f"{otc2}{(otc2+g)%10}" for g in range(4)]
    
    img_path = generate_pro_card(m_name, otc1, otc2, jodis)
    return img_path, "Success"

def main():
    os.system('clear')
    print(f"{G}🤖 ANNU PRO-ENGINE v16.8 STARTING...{W}")
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.txt')]
    for i, f in enumerate(files, 1):
        print(f"  [{i}] {f.upper()}")
    
    choice = input(f"\n{Y}Select Market: {W}")
    try:
        img, status = analyze_jodi_patterns(files[int(choice)-1])
        print(f"{G}✅ Card Generated: {img}{W}")
    except:
        print(f"{R}❌ Error in scanning.{W}")

if __name__ == "__main__":
    main()
