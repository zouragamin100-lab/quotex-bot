import asyncio
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from quotexpy import Quotex

logging.basicConfig(level=logging.INFO)

# ================== بياناتك ==================
EMAIL = "amine827y@gmail.com"
PASSWORD = "MIDOMIDOMIDO123"
TELEGRAM_TOKEN = "8928367627:AAHpiqsRIHKMAKDn4I4E0OGNNIIqXMX2f3M"

client = None

# ================== تسجيل الدخول ==================
async def login_quotex():
    global client
    try:
        client = Quotex(email=EMAIL, password=PASSWORD)
        check, reason = await client.connect()
        if check:
            print("✅ متصل بـ Quotex بنجاح")
            return True
        else:
            print(f"❌ فشل الاتصال: {reason}")
            return False
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
        return False

# ================== الأوامر ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **البوت شغال الآن!**\n\n"
        "استخدم الأمر: /signals"
    )

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("❌ البوت غير متصل بـ Quotex")
        return
    
    msg = await update.message.reply_text("🔄 جاري تحليل الأزواج...")

    # هنا سيتم إضافة التحليل لاحقاً
    await msg.edit_text("✅ البوت يعمل\n\nالإشارات ستظهر قريباً إن شاء الله")

# ================== تشغيل البوت ==================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))

    print("🤖 البوت يعمل على
