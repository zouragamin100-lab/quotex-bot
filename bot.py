import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = "8928367627:AAHpiqsRIHKMAKDn4I4E0OGNNIIqXMX2f3M"
GEMINI_API_KEY = "AIzaSyDsqQO70Y3mAwn8jD3d7rai56I7YzyjviY"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
أنت خبير محترف في تداول Quotex OTC على إطار 1 دقيقة.
حلل الصورة جيداً وأعطني اتجاه واحد فقط.
الرد يجب أن يكون كلمة واحدة فقط: Call أو Sell أو Wait
كن محافظاً جداً.
"""

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        response = model.generate_content([
            SYSTEM_PROMPT,
            {"mime_type": "image/jpeg", "data": downloaded_file}
        ])
        
        answer = response.text.strip().upper()
        
        if "CALL" in answer:
            bot.reply_to(message, "✅ **Call**")
        elif "SELL" in answer:
            bot.reply_to(message, "🔻 **Sell**")
        else:
            bot.reply_to(message, "⏳ **Wait**")
    except Exception:
        bot.reply_to(message, "❌ خطأ، حاول مرة أخرى")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت جاهز!\nأرسل سكرين شارت Quotex OTC (1 دقيقة)")

print("✅ Bot is running...")
bot.infinity_polling()
