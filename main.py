import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import http.server
import socketserver
import threading
import os

BOT_TOKEN = "8830802739:AAFGIQ-L1DqYi3OX1rWWjRJjshsHW9JziAI"
ADMIN_ID = 7996466440  

bot = telebot.TeleBot(BOT_TOKEN)
user_wallets = {}

products = {
    "fluorite": {"name": "🔮 FLUORITE", "1 Day": 4, "7 Days": 13, "31 Days": 20},
    "drip": {"name": "🔹 DRIP CLIENT", "1 Day": 2, "7 Days": 4, "31 Days": 9},
    "migul": {"name": "💎 MIGUL PRO", "1 Day": 4, "7 Days": 11, "31 Days": 20},
    "hg": {"name": "😃 HG CHEAT", "1 Day": 3, "7 Days": 5, "31 Days": 11},
    "pato": {"name": "🛒 PATO TEAM", "1 Day": 3, "7 Days": 5, "31 Days": 11},
    "br": {"name": "🌟 BR MODS", "1 Day": 3, "7 Days": 5, "31 Days": 10},
    "cert": {"name": "🤡 CERTIFICATE", "1 Year": 8}
}

def check_user(user_id):
    if user_id not in user_wallets:
        user_wallets[user_id] = 0

def main_markup(user_id):
    check_user(user_id)
    points = user_wallets[user_id]
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("🔥 تصفح وشراء المنتجات / Products", callback_data="buy_menu")
    btn2 = InlineKeyboardButton("💳 طرق الدفع والطلب / Payment", callback_data="show_payment")
    btn3 = InlineKeyboardButton("🔮 شحن رصيد نقاط / Recharge", url="https://t.me/MOUAD0219")
    markup.add(btn1, btn2, btn3)
    return markup, points

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup, points = main_markup(message.from_user.id)
    welcome_text = (
        f"👋 أهلاً بك في متجرنا الرسمي!\n"
        f"💰 رصيدك الحالي: {points} نقطة.\n"
        f"━━━━━━━━━━━━━━\n"
        f"إختر من الأزرار أسفله للتصفح أو الشراء مباشرة 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['add'])
def add_points(message):
    if message.from_user.id == ADMIN_ID:
        try:
            args = message.text.split()
            target_user = int(args[1])
            amount = int(args[2])
            check_user(target_user)
            user_wallets[target_user] += amount
            bot.reply_to(message, f"✅ تم بنجاح إضافة {amount} نقطة لحساب العميل {target_user}.\nرصيده الحالي: {user_wallets[target_user]} نقطة.")
            bot.send_message(target_user, f"🎉 تم شحن حسابك بـ {amount} نقطة من قبل الإدارة!\nرصيدك الحالي: {user_wallets[target_user]} نقطة.")
        except:
            bot.reply_to(message, "❌ خطأ في الصيغة! اكتب الأمر هكذا:\n/add [آيدي المستخدم] [عدد النقاط]")
    else:
        bot.reply_to(message, "❌ هذا الأمر مخصص لمالك البوت فقط.")

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.from_user.id
    check_user(user_id)
    
    if call.data == "buy_menu":
        markup = InlineKeyboardMarkup(row_width=2)
        for key, value in products.items():
            markup.add(InlineKeyboardButton(value["name"], callback_data=f"prod_{key}"))
        markup.add(InlineKeyboardButton("⬅️ عودة", callback_data="back_main"))
        bot.edit_message_text("👇 إختر المنتج الذي تريد شراءه:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data.startswith("prod_"):
        prod_key = call.data.split("_")[1]
        prod_data = products[prod_key]
        markup = InlineKeyboardMarkup(row_width=1)
        for duration, price in prod_data.items():
            if duration != "name":
                markup.add(InlineKeyboardButton(f"{duration} ➜ {price} نقطة", callback_data=f"confirm_{prod_key}_{duration}_{price}"))
        markup.add(InlineKeyboardButton("⬅️ عودة للمنتجات", callback_data="buy_menu"))
        bot.edit_message_text(f"حسناً، إختر مدة الاشتراك لمنتج **{prod_data['name']}**:", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("confirm_"):
        _, prod_key, duration, price = call.data.split("_")
        price = int(price)
        prod_name = products[prod_key]["name"]
        markup = InlineKeyboardMarkup()
        btn_yes = InlineKeyboardButton("✅ نعم، تأكيد الشراء", callback_data=f"buyyes_{prod_key}_{duration}_{price}")
        btn_no = InlineKeyboardButton("❌ إلغاء", callback_data="buy_menu")
        markup.add(btn_yes, btn_no)
        bot.edit_message_text(f"⚠️ **تأكيد عملية الشراء**:\n\nالمنتج: {prod_name}\nالمدة: {duration}\nالسعر: {price} نقطة\n\nهل أنت متأكد من الشراء؟ سيتم خصم النقاط فوراً.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buyyes_"):
        _, prod_key, duration, price = call.data.split("_")
        price = int(price)
        prod_name = products[prod_key]["name"]
        
        if user_wallets[user_id] >= price:
            user_wallets[user_id] -= price
            bot.edit_message_text(f"✅ **تم الشراء بنجاح!**\n\nلقد اشتريت: {prod_name} ({duration})\nتم خصم: {price} نقطة.\nرصيدك المتبقي: {user_wallets[user_id]} نقطة.\n\n⏱️ تم إرسال طلبك للإدارة، يرجى الانتظار لتسليمك المفتاح.", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
            
            client_user = f"@{call.from_user.username}" if call.from_user.username else "لا يوجد يوزر"
            admin_alert = (
                f"🚨 **طلب شراء جديد دخل للمتجر!** 🚨\n\n"
                f"👤 العميل: {call.from_user.first_name}\n"
                f"🆔 آيدي العميل: `{user_id}`\n"
                f"✉️ يوزر العميل: {client_user}\n\n"
                f"📦 المنتج المطلـوب: {prod_name}\n"
                f"⏱️ المدة: {duration}\n"
                f"💰 السعر المقبوض: {price} نقطة\n\n"
                f"قم بالتواصل معه وتسليمه كوده المفتاح الآن 👍"
            )
            bot.send_message(ADMIN_ID, admin_alert, parse_mode="Markdown")
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔮 اشحن نقاطك الآن", url="https://t.me/MOUAD0219"))
            markup.add(InlineKeyboardButton("⬅️ عودة", callback_data="buy_menu"))
            bot.edit_message_text(f"❌ **عذراً، رصيدك غير كافٍ!**\n\nسعر المنتج: {price} نقطة\nرصيدك الحالي: {user_wallets[user_id]} نقطة.\n\nيرجى شحن حسابك أولاً للتتمكن من إتمام الطلب.", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "show_payment":
        payment_text = (
            "📩 **ORDER / للطلب والاستفسار:**\nContact: @QEA77_DZ\n\n"
            "💳 **PAYMENT METHODS / طرق الدفع:**\n• Binance  • PayPal  • Gift Cards  • Morocco Payment Methods 🇲🇦\n\n"
            "💵 **RECHARGE POINTS / لتعبئة الرصيد:**\nقاعدة الشحن: 1 نقطة = 1 دولار\n"
            "🆔 الآيدي الخاص بك (اعطه للآدمن ليشحن لك): `" + str(user_id) + "`\n\n"
            "لتعبئة رصيدك وتجميع النقاط يرجى التواصل عبر الرابط:\n🔗 https://t.me/MOUAD0219"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("⬅️ عودة للقائمة الرئيسية", callback_data="back_main"))
        bot.edit_message_text(payment_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "back_main":
        markup, points = main_markup(user_id)
        welcome_text = (
            f"👋 أهلاً بك في متجرنا الرسمي!\n"
            f"💰 رصيدك الحالي: {points} نقطة.\n"
            f"━━━━━━━━━━━━━━\n"
            f"إختر من الأزرار أسفله للتصفح أو الشراء مباشرة 👇"
        )
        bot.edit_message_text(welcome_text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# تشغيل خادم ويب وهمي لإبقاء الخدمة المجانية حية على Render
def run_web_server():
    PORT = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌍 خادم الويب يعمل على المنفذ: {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # تشغيل الويب في خلفية منفصلة لكي لا يعطل البوت
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    print("⚡ البوت المتطور يعمل الآن مجاناً...")
    bot.infinity_polling()
