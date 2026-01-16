from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import os

# Flask app তৈরি
app = Flask(__name__)

# Telegram API Token
TOKEN = "8221663079:AAHR01BGwId6N4aL8HYu7yUwBK4n6eJ8Fng"
WEBHOOK_URL = "https://my-telegram-bot-enl0.onrender.com"  # Render URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি Webhook দিয়ে কাজ করছি!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

# Application তৈরি
telegram_app = ApplicationBuilder().token(TOKEN).build()

# Handler যোগ করা
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Webhook সেট করা
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), telegram_app.bot)
        telegram_app.process_update(update)
    return "OK", 200

# Flask app চালানো (Render server)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))  # SSL সার্টিফিকেট প্রয়োজন