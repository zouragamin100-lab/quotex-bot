import asyncio
import pandas as pd
import pandas_ta as ta
from quotexpy import Quotex
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
from datetime import datetime, date

logging.basicConfig(level=logging.INFO)

# ================== إعدادات ==================
EMAIL = amine827y@gmail.com
PASSWORD = MIDOMIDOMIDO123
TELEGRAM_TOKEN = 8928367627:AAHpiqsRIHKMAKDn4I4E0OGNNIIqXMX2f3M

# إعدادات إدارة المخاطر
RISK_PERCENT = 1.0
MAX_DAILY_LOSS_PERCENT = 5.0
MAX_TRADES_PER_DAY = 10

client = None
balance = 0
daily_trades = 0
daily_loss = 0
today = date.today()

# ================== تسجيل الدخول ==================
async def login_quotex():
    global client, balance
    try:
        client = Quotex(email=EMAIL, password=PASSWORD)
        check, reason = await client.connect()
        if check:
            balance = await client.get_balance()
            print(f"✅ متصل بـ Quotex | الرصيد: ${balance}")
            return True
        else:
            print(f"❌ فشل الاتصال: {reason}")
            return False
    except Exception as e:
        print(f"خطأ في الاتصال: {e}")
        return False

# ================== تحليل الزوج ==================
async def get_analysis(pair: str):
    try:
        candles = await client.get_historical_candles(pair, 200, 60)
        if not candles:
            return None

        df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

        df['rsi'] = ta.rsi(df['close'], length=14)
        df['ema_fast'] = ta.ema(df['close'], length=9)
        df['ema_slow'] = ta.ema(df['close'], length=21)

        latest = df.iloc[-1]

        signal = "HOLD"
        confidence = 60

        if (latest['ema_fast'] > latest['ema_slow'] and latest['rsi'] < 68):
            signal = "CALL"
            confidence = 75
        elif (latest['ema_fast'] < latest['ema_slow'] and latest['rsi'] > 32):
            signal = "PUT"
            confidence = 75

        return {
            "pair": pair,
            "signal": signal,
            "confidence": confidence,
            "price": round(float(latest['close']), 5),
            "rsi": round(float(latest['rsi']), 2),
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except Exception as e:
        print(f"خطأ تحليل {pair}: {e}")
        return None

# ================== أوامر البوت ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 البوت شغال!\nاستخدم /signals")

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text("❌ البوت غير متصل")
        return

    msg = await update.message.reply_text("🔄 جاري التحليل...")

    pairs = ["EURUSD_OTC", "AUDUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC"]
    results = []

    for pair in pairs:
        analysis = await get_analysis(pair)
        if analysis and analysis["signal"] != "HOLD":
            text = f"""
🪙 **{analysis['pair']}**
📊 **{analysis['signal']}**
💰 {analysis['price']}
📈 RSI: {analysis['rsi']}
⭐ الثقة: {analysis['confidence']}%
            """
            results.append(text)

    if results:
        await msg.edit_text("\n".join(results))
    else:
        await msg.edit_text("🟡 لا توجد إشارات قوية الآن")

# ================== تشغيل البوت ==================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))

    print("🤖 البوت يعمل...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(login_quotex())
    main()
