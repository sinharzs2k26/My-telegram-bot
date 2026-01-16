from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Filters

app = Flask(__name__)

TOKEN = "8221663079:AAHR01BGwId6N4aL8HYu7yUwBK4n6eJ8Fng"
URL = "https://my-telegram-bot.onrender.com/webhook"  # Render URL

# Flask route to handle webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(), bot)
        dispatcher.process_update(update)
    return "OK", 200

def start(update, context):
    update.message.reply_text("হ্যালো! আমি Webhook দিয়ে কাজ করছি!")

def echo(update, context):
    update.message.reply_text(update.message.text)

# Set up application and dispatcher
bot = ApplicationBuilder().token(TOKEN).build()
dispatcher = bot.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))  # SSL cert path
