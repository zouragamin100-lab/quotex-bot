import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import pandas as pd
import pandas_ta as ta

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
# QUOTEX_EMAIL = os.getenv("QUOTEX_EMAIL")
# QUOTEX_PASSWORD = os.getenv("QUOTEX_PASSWORD")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال!\nاستخدم /signals للحصول على إشارات")

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 جاري تحليل الأزواج OTC...\n\nحالياً البوت في مرحلة التجربة.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))
    
    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
