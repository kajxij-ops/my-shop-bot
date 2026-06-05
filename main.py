import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8830802739:AAFGIQ-L1DqYi3OX1rWWjRJjshsHW9JziAI"
# ✅ تم وضع الآيدي الخاص بك بنجاح لتلقي الإشعارات والتحكم بالنقاط
ADMIN_ID = 7996466440  

bot = telebot.TeleBot(BOT_TOKEN)

# قاعدة بيانات وهمية في الذاكرة لتخزين نقاط المستخدمين (تصفير عند إعادة التشغيل)
user_wallets = {}

# بيانات المنتجات والأسعار بالنقاط
products = {
    "fluorite": {"name": "🔮 FLUORITE", "1 Day": 4, "7 Days": 13, "31 Days": 20},
    "drip": {"name": "🔹 DRIP CLIENT", "1 Day": 2, "7 Days": 4, "31 Days": 9},
    "migul": {"name": "💎 MIGUL PRO", "1 Day": 4, "7 Days": 11, "31 Days": 20},
    "hg": {"name": "😃 HG CHEAT", "1 Day": 3, "7 Days": 5, "31 Days": 11},
    "pato": {"name": "🛒 PATO TEAM", "1 Day": 3, "7 Days": 5, "31 Days": 11},
    "br": {"name": "🌟 BR MODS", "1 Day": 3, "7 Days": 5, "31 Days": 10},
    "cert": {"name": "🤡 CERTIFICATE", "1 Year": 8}
}

# د
