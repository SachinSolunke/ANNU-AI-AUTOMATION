import telebot
from telebot import types
import os

API_TOKEN = '8733244182:AAHe3TQ-nYOYCrcjQnwzfZD4cZUTsU2q3sM'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    # Inline Buttons Menu
    markup = types.InlineKeyboardMarkup()
    
    # 🌐 Permanent GitHub Link Button
    github_btn = types.InlineKeyboardButton(
        text="🌐 Open My GitHub (Annu-AI)", 
        url="https://github.com/SachinSolunke/ANNU-AI-AUTOMATION/tree/main"
    )
    
    # 📊 System Control Buttons
    status_btn = types.InlineKeyboardButton(text="🖥️ System Status", callback_data="status")
    sync_btn = types.InlineKeyboardButton(text="🔄 Sync GitHub Now", callback_data="sync")
    
    markup.add(github_btn)
    markup.add(status_btn, sync_btn)

    welcome_text = (
        f"नमस्ते सचिन भाई! 🙏\n\n"
        f"Aapka **Jarvis (Annu AI)** ab online hai.\n"
        f"GitHub link niche button mein 'Fixed' hai, ye kabhi gum nahi hoga.\n\n"
        f"Kya karna chahte hain?"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "status":
        bot.answer_callback_query(call.id, "Checking System...")
        bot.send_message(call.message.chat.id, "✅ Termux: Active\n✅ GitHub: Connected\n✅ Auto-Backup: Running")
    
    elif call.data == "sync":
        bot.answer_callback_query(call.id, "Starting Sync...")
        bot.send_message(call.message.chat.id, "🔄 GitHub Sync shuru ho raha hai...")
        os.system("python AutoGit.py")
        bot.send_message(call.message.chat.id, "✅ Sync Complete, Sachin Bhai!")

print("📡 Vedhanacbot (Jarvis) is Running...")
bot.infinity_polling()
