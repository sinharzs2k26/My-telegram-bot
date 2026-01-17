import os
import asyncio
from threading import Thread
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

# Bot token from environment
TOKEN = os.environ.get('TELEGRAM_TOKEN')
WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL', '') + '/webhook'

# Create application
application = Application.builder().token(TOKEN).build()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm hosted on Render 24/7! 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot hosted for free on Render.com!")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

# Flask routes
@app.route('/')
def home():
    return "Bot Server Running ✅"

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/set_webhook')
def set_webhook():
    # You'll call this once after deployment
    async def set_wh():
        await application.bot.set_webhook(WEBHOOK_URL)
    
    asyncio.run(set_wh())
    return f"Webhook set to: {WEBHOOK_URL}"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Main webhook endpoint"""
    update = Update.de_json(request.get_json(force=True), application.bot)
    
    # Process update in a thread
    thread = Thread(target=process_update, args=(update,))
    thread.start()
    
    return 'OK', 200

def process_update(update):
    """Process update in a separate thread"""
    asyncio.run(application.process_update(update))

if __name__ == '__main__':
    # Run Flask server
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)