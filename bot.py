import os
import json
import logging
import threading
import time
import asyncio
import requests
from flask import Flask, request, jsonify
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== SETUP ====================
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot instance
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot_application = None

# ==================== BOT INITIALIZATION ====================

def initialize_bot():
    """Initialize the Telegram bot application"""
    global bot_application
    
    if not TOKEN:
        logger.error("❌ TELEGRAM_TOKEN environment variable is not set!")
        logger.error("Please set it in Render dashboard: Environment → Add TELEGRAM_TOKEN")
        return None
    
    try:
        logger.info("🔄 Initializing Telegram bot...")
        
        # Create bot application
        bot_application = Application.builder().token(TOKEN).build()
        
        # Add command handlers
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🚀 Bot is online! Type /help for commands.")
        
        async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            help_text = """
🤖 *Available Commands:*
/start - Start the bot
/help - Show this help
/ping - Check if bot is alive
/time - Current server time
/joke - Get a random joke
            """
            await update.message.reply_text(help_text, parse_mode='Markdown')
        
        async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("🏓 Pong! I'm running on Render 24/7!")
        
        async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            await update.message.reply_text(f"🕐 Server time: {current_time}")
        
        async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
            import random
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!"
            ]
            await update.message.reply_text(f"😂 {random.choice(jokes)}")
        
        # Register handlers
        bot_application.add_handler(CommandHandler("start", start))
        bot_application.add_handler(CommandHandler("help", help_cmd))
        bot_application.add_handler(CommandHandler("ping", ping))
        bot_application.add_handler(CommandHandler("time", get_time))
        bot_application.add_handler(CommandHandler("joke", joke))
        
        # Initialize the application (THIS IS CRITICAL!)
        # We'll initialize it properly in a separate thread
        logger.info("✅ Bot handlers registered")
        
        return bot_application
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {e}", exc_info=True)
        return None

# Initialize bot on import
bot_application = initialize_bot()

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    bot_status = "✅ Online" if bot_application else "❌ Offline (Token not set)"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Telegram Bot</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .status {{ padding: 10px; background: #f0f0f0; border-radius: 5px; }}
            .success {{ color: green; font-weight: bold; }}
            .error {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>🤖 Telegram Bot Dashboard</h1>
        <div class="status">
            <p><strong>Status:</strong> <span class="{'success' if bot_application else 'error'}">{bot_status}</span></p>
            <p><strong>Server:</strong> Render.com</p>
            <p><strong>URL:</strong> {request.host_url}</p>
        </div>
        <h3>Quick Actions:</h3>
        <ul>
            <li><a href="/set_webhook">🔗 Set Webhook</a> (Do this first!)</li>
            <li><a href="/health">❤️ Health Check</a></li>
            <li><a href="/test">🧪 Test Bot</a></li>
            <li><a href="/logs">📋 View Recent Logs</a></li>
        </ul>
        <p>After setting webhook, send <code>/start</code> to your bot on Telegram.</p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint"""
    if bot_application:
        return jsonify({
            "status": "healthy",
            "bot": "initialized",
            "server": "Render",
            "timestamp": time.time()
        }), 200
    else:
        return jsonify({
            "status": "unhealthy",
            "error": "Bot not initialized",
            "fix": "Check TELEGRAM_TOKEN environment variable"
        }), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set webhook endpoint - NO ASYNC HERE!"""
    try:
        if not bot_application:
            return "❌ Bot not initialized. Check TELEGRAM_TOKEN.", 500
        
        current_url = request.host_url.rstrip('/')
        webhook_url = f"{current_url}/webhook"
        
        # Set webhook using async in a separate thread
        async def set_webhook_async():
            try:
                await bot_application.initialize()
                await bot_application.start()
                await bot_application.bot.set_webhook(webhook_url)
                
                # Set bot commands
                commands = [
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Show help message"),
                    BotCommand("ping", "Check if bot is alive"),
                    BotCommand("time", "Get server time"),
                    BotCommand("joke", "Get a random joke"),
                ]
                await bot_application.bot.set_my_commands(commands)
                
                return True, "✅ Webhook and commands set successfully!"
            except Exception as e:
                return False, f"❌ Error: {str(e)}"
        
        # Run async function synchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success, message = loop.run_until_complete(set_webhook_async())
        loop.close()
        
        if success:
            return f"""
            <h2>✅ Success!</h2>
            <p><strong>Webhook URL:</strong> {webhook_url}</p>
            <p><strong>Status:</strong> {message}</p>
            <p><strong>Next:</strong> Send <code>/start</code> to your bot on Telegram!</p>
            <p><a href="/">← Back to Dashboard</a></p>
            """
        else:
            return f"<h2>❌ Failed</h2><p>{message}</p>"
            
    except Exception as e:
        logger.error(f"Error in set_webhook: {e}", exc_info=True)
        return f"<h2>❌ Error</h2><pre>{str(e)}</pre>", 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Telegram webhook - BULLETPROOF VERSION"""
    try:
        if not bot_application:
            logger.error("Bot application not initialized")
            return "Bot not initialized", 500
        
        # Parse the update
        update_data = request.get_json(force=True)
        logger.info(f"📨 Received update: {update_data.get('update_id')}")
        
        # Create update object
        update = Update.de_json(update_data, bot_application.bot)
        
        # Process update in background thread
        def process_update_in_thread(update_obj):
            """Process update in a separate thread with its own event loop"""
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Ensure bot is initialized
                if not bot_application.running:
                    loop.run_until_complete(bot_application.initialize())
                    loop.run_until_complete(bot_application.start())
                
                # Process the update
                loop.run_until_complete(bot_application.process_update(update_obj))
                
                loop.run_until_complete(bot_application.stop())
                loop.close()
                
                logger.info(f"✅ Processed update {update_obj.update_id}")
                
            except Exception as e:
                logger.error(f"❌ Error processing update: {e}", exc_info=True)
        
        # Start processing in background thread
        import threading
        thread = threading.Thread(target=process_update_in_thread, args=(update,))
        thread.daemon = True
        thread.start()
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}", exc_info=True)
        return 'ERROR', 500

@app.route('/test')
def test_bot():
    """Test endpoint to send a message"""
    try:
        # Get your chat ID from environment or use a default
        test_chat_id = os.environ.get('TEST_CHAT_ID', '')
        
        if test_chat_id:
            # Send test message
            test_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            response = requests.post(test_url, json={
                'chat_id': test_chat_id,
                'text': '🔧 Test message from bot server!'
            })
            return f"Test message sent: {response.json()}"
        else:
            return """
            <h2>Test Bot</h2>
            <p>To test, set TEST_CHAT_ID environment variable with your Telegram chat ID.</p>
            <p>Get your chat ID from @userinfobot on Telegram.</p>
            """
    except Exception as e:
        return f"Test failed: {str(e)}"

@app.route('/logs')
def show_logs():
    """Show recent logs"""
    import io
    import traceback
    
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.INFO)
    
    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    
    # Add handler to the logger
    logger.addHandler(ch)
    
    # Get logs
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()
    logger.removeHandler(ch)
    
    return f"""
    <h2>Recent Logs</h2>
    <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto;">
{log_contents if log_contents else 'No recent logs...'}
    </pre>
    <p><a href="/">← Back</a></p>
    """

# ==================== KEEP-ALIVE SYSTEM ====================

def start_keep_alive():
    """Keep Render from sleeping"""
    def ping_server():
        while True:
            try:
                url = os.environ.get('RENDER_EXTERNAL_URL', request.host_url.rstrip('/') if 'request' in locals() else '')
                if not url:
                    url = f"http://localhost:{os.environ.get('PORT', 10000)}"
                
                response = requests.get(f"{url}/health", timeout=10)
                logger.info(f"🔄 Keep-alive ping: {response.status_code}")
            except Exception as e:
                logger.warning(f"Keep-alive failed: {e}")
            
            time.sleep(240)  # Ping every 4 minutes
    
    # Start in background thread
    thread = threading.Thread(target=ping_server, daemon=True)
    thread.start()
    logger.info("🚀 Keep-alive system started")

# ==================== STARTUP ====================

if __name__ == '__main__':
    # Start keep-alive
    start_keep_alive()
    
    # Log startup info
    logger.info("=" * 50)
    logger.info("🤖 Telegram Bot Server Starting Up")
    logger.info(f"🔑 Token set: {'Yes' if TOKEN else 'No'}")
    logger.info(f"🤖 Bot initialized: {'Yes' if bot_application else 'No'}")
    logger.info(f"🌐 Server URL: {os.environ.get('RENDER_EXTERNAL_URL', 'Local')}")
    logger.info("=" * 50)
    
    # Start Flask server
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)