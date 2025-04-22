from flask import Flask
import requests
from telegram import Bot
import asyncio
import time

app = Flask(__name__)

BOT_TOKEN = '7636156643:AAGAo3m06fHGj9llC3j5X_TNqzwpEULUrRM'
CHAT_ID = '@usdtgol'
bot = Bot(token=BOT_TOKEN)

def get_usdt_price():
    try:
        now = int(time.time())
        one_day_ago = now - 86400
        url = (
            "https://api.abantether.com/otc_reporting/tradingview/history"
            f"?symbol=USDT%2FIRT&resolution=1D&from={one_day_ago}&to={now}&countback=2"
        )
        headers = {
            "Origin": "https://abantether.com",
            "Referer": "https://abantether.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if "c" in data and len(data["c"]) > 0:
            return float(data["c"][-1])
    except Exception as e:
        print(f"❌ خطا: {e}")
    return None

async def send_price():
    price = get_usdt_price()
    if price:
        price_with_fee = round(price * 1.015)
        inverse = 1 / price_with_fee
        msg1 = f"✅ قیمت تتر: {price:,.0f} تومان\n🥇 با ۱.۵٪ کارمزد: {price_with_fee:,.0f} تومان"
        msg2 = f"📊 {inverse:.18f}"
        await bot.send_message(chat_id=CHAT_ID, text=msg1)
        await bot.send_message(chat_id=CHAT_ID, text=msg2)

@app.route('/')
def index():
    asyncio.run(send_price())
    return "📬 پیام ارسال شد!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
