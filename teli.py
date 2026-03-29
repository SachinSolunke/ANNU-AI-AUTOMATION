import telebot
from telebot import types
import os
import sys
import Annu  # Annu.py ka engine

# 🔑 Connection Setup
API_TOKEN = '8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM'.strip()
bot = telebot.TeleBot(API_TOKEN)

def github_sync():
    """GitHub par auto-update karne ke liye"""
    try:
        os.system("git add .")
        os.system("git commit -m 'Auto-Scan Update by Annu-AI'")
        os.system("git push")
        return "✅ GitHub Synced!"
    except:
        return "⚠️ GitHub Sync Failed."

@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markets = ["KALYAN", "SRIDEVI", "MILAN", "TIME-BAZAR"]
    btns = [types.InlineKeyboardButton(f"🎯 {m}", callback_data=f"run_{m}") for m in markets]
    
    status_btn = types.InlineKeyboardButton("🖥️ System Status", callback_data="status")
    markup.add(*btns)
    markup.add(status_btn)

    bot.send_message(message.chat.id, "नमस्ते सचिन भाई! 🌹\nAnnu AI 'One-in-All' Control Room active hai.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Timeout prevention
    try: bot.answer_callback_query(call.id)
    except: pass

    if "run_" in call.data:
        market = call.data.split("_")[1]
        msg = bot.send_message(call.message.chat.id, f"🔎 **Annu** {market} ko scan aur card bana rahi hai...")
        
        try:
            # 1. Background mein scan aur photo banana
            img_path, status = Annu.analyze_jodi_patterns(f"{market}.txt", bot_mode=True)
            
            if img_path and os.path.exists(img_path):
                # 2. Photo bhej dena
                with open(img_path, 'rb') as photo:
                    bot.send_photo(call.message.chat.id, photo, caption=f"✅ {market} Pro-Result Ready! 🌹")
                
                # 3. GitHub update
                sync_status = github_sync()
                bot.send_message(call.message.chat.id, sync_status)
            else:
                bot.send_message(call.message.chat.id, f"⚠️ Error: {market}.txt nahi mila.")
            
            bot.delete_message(call.message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error: {str(e)}")

    elif call.data == "status":
        bot.send_message(call.message.chat.id, "🖥️ **System:** Online\n✅ **Annu Engine:** Active\n✅ **Auto-Push:** Ready")

print("📡 Annu-Jarvis (Vedhanacbot) is LIVE & READY...")
bot.infinity_polling()
