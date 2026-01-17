import os
import logging
import threading
import time
import requests
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ========== KEEP-ALIVE CODE DIRECTLY IN BOT.PY ==========
def start_keep_alive():
    """Background thread to ping the server and prevent sleep"""
    def ping_server():
        while True:
            try:
                # Get the Render URL from environment
                url = os.environ.get('RENDER_EXTERNAL_URL')
                
                # If we're on Render, ping our own health endpoint
                if url and "render.com" in url:
                    response = requests.get(f"{url}/health", timeout=10)
                    logging.info(f"✅ Keep-alive ping sent: {response.status_code}")
                else:
                    # Local development
                    requests.get("http://localhost:10000/health", timeout=5)
                    logging.info("🔄 Local keep-alive ping")
            except Exception as e:
                logging.error(f"❌ Keep-alive failed: {e}")
            
            # Wait 4 minutes (Render sleeps after 15 minutes)
            time.sleep(240)
    
    # Start the ping in a background thread
    thread = threading.Thread(target=ping_server, daemon=True)
    thread.start()
    logging.info("🚀 Keep-alive thread started")
# ========== END KEEP-ALIVE CODE ==========

# ========== FLASK APP ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

@app.route('/health')
def health():
    return 'OK', 200

# ========== TELEGRAM BOT ==========
TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Initialize bot
application = Application.builder().token(TOKEN).build()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive 24/7 on Render! ⚡")

application.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # ... webhook handling code ...
    return 'OK', 200

# ========== MAIN EXECUTION ==========
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )
    
    # START THE KEEP-ALIVE THREAD
    start_keep_alive()
    
    # Start Flask server
    port = int(os.environ.get('PORT', 10000))
    logging.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port)