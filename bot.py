import telebot
import requests
import re

# ================== إعدادات البوت ==================
TOKEN = "8393532186:AAHZbpgZ0OVrBBmJb4pjRzdNc1CiD6IXPiQ"  # توكنك مباشرة
OWNER_ID = 123456789      # ضع الـ ID الخاص بك
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=10)

# ================== دالة الحصول على ID ==================
def get_user_id_by_username(username):
    try:
        username = username.lstrip('@')
        url = f"https://t.me/{username}"
        response = requests.get(url, timeout=3)
        match = re.search(r'"id":(\d+)', response.text)
        if match:
            return match.group(1)
        return None
    except:
        return None

# ================== أوامر البوت ==================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == OWNER_ID:
        bot.reply_to(message, "👑 أهلاً بك مطوري العزيز!\nأرسل لي الـ ID أو الـ @username لمعرفة تاريخ إنشائه.")
    else:
        bot.reply_to(message, 
                     "👋 أهلاً بك!\n"
                     "📅 أرسل لي الـ ID أو الـ @username الخاص بحساب تيليجرام\n"
                     "وسأخبرك بتاريخ إنشائه ✨", 
                     parse_mode="Markdown")

@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, f"🆔 ID حسابك هو: {message.from_user.id}", parse_mode="Markdown")

# ================== معالجة الرسائل ==================
@bot.message_handler(func=lambda m: True)
def get_date(message):
    user_input = message.text.strip()
    sent_msg = bot.reply_to(message, "⏳ جاري البحث عن المعلومات، الرجاء الانتظار...")

    if user_input.startswith('@'):
        user_id = get_user_id_by_username(user_input)
        if not user_id:
            bot.edit_message_text("⚠ لم أستطع العثور على ID لهذا اليوزر.", message.chat.id, sent_msg.message_id)
            return
    else:
        user_id = re.sub(r'\D', '', user_input)

    url = f"http://145.223.80.56:5016/date?id={user_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            bot.edit_message_text(
                f"✅ تم العثور على المعلومات:\n\n"
                f"🆔 ID الحساب: {user_id}\n"
                f"📅 تاريخ الإنشاء: {response.text}\n\n"
                "💡 *هذه المعلومة تقريبية بناءً على قاعدة بيانات خاصة.*",
                message.chat.id, sent_msg.message_id,
                parse_mode="Markdown"
            )
        else:
            bot.edit_message_text("⚠ لم أستطع جلب البيانات من السيرفر.", message.chat.id, sent_msg.message_id)
    except requests.exceptions.Timeout:
        bot.edit_message_text("⏳ السيرفر تأخر في الرد.", message.chat.id, sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ: {e}", message.chat.id, sent_msg.message_id)

# ================== تشغيل البوت ==================
bot.polling(non_stop=True)
