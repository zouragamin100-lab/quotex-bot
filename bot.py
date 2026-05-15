import telebot
import google.generativeai as genai

# === التوكن والـ API Key ===
TELEGRAM_TOKEN = "8928367627:AAHpiqsRIHKMAKDn4I4E0OGNNIIqXMX2f3M"
GEMINI_API_KEY = "AIzaSyDsqQO70Y3mAwn8jD3d7rai56I7YzyjviY"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt قوي لتحليل الشارت
SYSTEM_PROMPT = """
أنت خبير محترف جداً في تداول Quotex OTC على إطار زمني 1 دقيقة فقط.
حلل السكرين شارت بعناية كبيرة وأعطني اتجاه واحد فقط.

القواعد الصارمة:
- الرد يكون كلمة واحدة فقط: "Call" أو "Sell" أو "Wait"
- استخدم أفضل المؤشرات والأنماط (EMA, RSI, MACD, Bollinger, Support/Resistance, Pinbar, Engulfing...)
- كن محافظ جداً، لا تعطي إشارة إلا لو كانت الاحتمالية عالية.
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
            
    except Exception
