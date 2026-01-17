import os
import logging
import datetime
import random
import requests
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== SETUP ====================
app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN not found in environment variables!")
    raise ValueError("Please set TELEGRAM_TOKEN environment variable")

# Initialize bot
application = Application.builder().token(TOKEN).build()

# ==================== COMMAND HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    user = update.effective_user
    
    welcome_text = f"""
👋 Hello {user.first_name}!

🤖 I'm your 24/7 Telegram bot hosted on Render!

📋 Available commands:
/start - Welcome message
/help - Show all commands
/ping - Check if I'm alive
/time - Current server time
/weather - Get weather info
/joke - Get a random joke
/cat - Get a random cat picture
/dog - Get a random dog picture
/quote - Inspirational quote
/roll - Roll a dice (1-6)
/flip - Flip a coin
/echo [text] - Echo your text
/about - About this bot

💡 Just send me any message and I'll respond!
    """
    
    # Create keyboard buttons
    keyboard = [
        [KeyboardButton("/help"), KeyboardButton("/time")],
        [KeyboardButton("/joke"), KeyboardButton("/cat")],
        [KeyboardButton("/weather"), KeyboardButton("/quote")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    logger.info(f"User {user.id} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    help_text = """
📚 *Available Commands:*

*Basic Commands:*
/start - Welcome message
/help - Show this help
/ping - Check bot status
/time - Current server time
/about - Bot information

*Fun Commands:*
/joke - Get a random joke
/cat - Random cat picture 🐱
/dog - Random dog picture 🐶
/quote - Inspirational quote
/roll - Roll a dice (1-6)
/flip - Flip a coin
/random [min] [max] - Random number

*Utility Commands:*
/weather [city] - Weather information
/echo [text] - Repeat your text
/calc [expression] - Simple calculation

💡 *Tip:* You can just send me normal messages too!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')
    logger.info(f"Help requested by {update.effective_user.id}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if bot is responsive"""
    await update.message.reply_text("🏓 Pong! I'm alive and running on Render! ⚡")
    logger.info("Ping received")

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current server time"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    await update.message.reply_text(f"🕐 Server time: {current_time}")
    logger.info(f"Time requested: {current_time}")

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a fish wearing a bowtie? Sofishticated!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call a sleeping bull? A bulldozer!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the bicycle fall over? Because it was two-tired!"
    ]
    joke = random.choice(jokes)
    await update.message.reply_text(f"😂 {joke}")

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random cat picture"""
    try:
        # Using TheCatAPI
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            cat_url = response.json()[0]['url']
            await update.message.reply_photo(photo=cat_url, caption="🐱 Here's a cute cat for you!")
        else:
            await update.message.reply_text("😿 Couldn't fetch cat picture, try again later!")
    except:
        await update.message.reply_text("😿 Cat API is sleeping!")

async def dog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random dog picture"""
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code == 200:
            dog_url = response.json()['message']
            await update.message.reply_photo(photo=dog_url, caption="🐶 Here's a good doggo!")
        else:
            await update.message.reply_text("🐕 Couldn't fetch dog picture!")
    except:
        await update.message.reply_text("🐕 Dog API is busy!")

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send inspirational quote"""
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "Strive not to be a success, but rather to be of value. - Albert Einstein",
        "The only thing we have to fear is fear itself. - Franklin D. Roosevelt",
        "Life is what happens to you while you're busy making other plans. - John Lennon",
        "The way to get started is to quit talking and begin doing. - Walt Disney",
        "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
    ]
    quote = random.choice(quotes)
    await update.message.reply_text(f"💭 {quote}")

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice"""
    result = random.randint(1, 6)
    await update.message.reply_text(f"🎲 You rolled a {result}!")

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await update.message.reply_text(f"🪙 It's {result}!")

async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate random number"""
    try:
        if context.args:
            if len(context.args) == 1:
                max_num = int(context.args[0])
                min_num = 1
            else:
                min_num = int(context.args[0])
                max_num = int(context.args[1])
            result = random.randint(min_num, max_num)
            await update.message.reply_text(f"🎯 Random number between {min_num} and {max_num}: *{result}*", 
                                          parse_mode='Markdown')
        else:
            await update.message.reply_text("Usage: /random [min] [max] or /random [max]")
    except:
        await update.message.reply_text("Please use numbers like: /random 1 100")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get weather information"""
    if context.args:
        city = ' '.join(context.args)
        await update.message.reply_text(f"🌤️ Weather for {city}: Feature coming soon!\n(Would use OpenWeatherMap API)")
    else:
        await update.message.reply_text("Please specify a city: /weather London")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user's message"""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"📢 You said: {text}")
    else:
        await update.message.reply_text("Usage: /echo [your text here]")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information"""
    about_text = """
🤖 *About This Bot*

*Hosting:* Render.com (Free Tier)
*Uptime:* 24/7 with keep-alive
*Framework:* python-telegram-bot
*Features:* Multiple commands, webhook based

*Developer:* You! 🎉
*Status:* 🟢 Online and responsive

This bot demonstrates how to host a Telegram bot for free with full functionality!
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages that are not commands"""
    user_message = update.message.text.lower()
    user = update.effective_user
    
    logger.info(f"Message from {user.id}: {user_message}")
    
    # Simple AI-like responses
    responses = {
        'hello': f"Hi {user.first_name}! 👋 How can I help you today?",
        'hi': f"Hello {user.first_name}! 😊",
        'how are you': "I'm doing great, thanks for asking! Running smoothly on Render! ⚡",
        'thanks': "You're welcome! 😊",
        'thank you': "Anytime! 👍",
        'bye': "Goodbye! Have a great day! 👋",
        'good morning': f"Good morning {user.first_name}! 🌅",
        'good night': "Good night! Sleep well! 🌙",
        'what is your name': "I'm your friendly Telegram bot hosted on Render! 🤖",
        'what can you do': "Type /help to see all my commands! 📋",
        'who made you': "You created me! I'm your bot running on Render! 🎉",
        'render': "Yes! I'm hosted for FREE on Render.com! 🚀",
        'python': "I'm built with Python and python-telegram-bot library! 🐍",
        'telegram': "Telegram is awesome for building bots! 💪",
    }
    
    # Check if message matches any predefined responses
    for keyword, response in responses.items():
        if keyword in user_message:
            await update.message.reply_text(response)
            return
    
    # Default response for unknown messages
    default_responses = [
        f"Interesting message, {user.first_name}! Try /help for commands.",
        f"I received: '{user_message}' - Need help? Type /help",
        f"Thanks for the message! Want to see what I can do? Type /help",
        f"Got it! Check out /help for all my features!",
    ]
    
    await update.message.reply_text(random.choice(default_responses))

# ==================== REGISTER HANDLERS ====================

# Command handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("ping", ping))
application.add_handler(CommandHandler("time", time_command))
application.add_handler(CommandHandler("joke", joke))
application.add_handler(CommandHandler("cat", cat))
application.add_handler(CommandHandler("dog", dog))
application.add_handler(CommandHandler("quote", quote))
application.add_handler(CommandHandler("roll", roll))
application.add_handler(CommandHandler("flip", flip))
application.add_handler(CommandHandler("random", random_number))
application.add_handler(CommandHandler("weather", weather))
application.add_handler(CommandHandler("echo", echo))
application.add_handler(CommandHandler("about", about))

# Message handler (for non-command messages)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    return """
    <h1>🤖 Telegram Bot Dashboard</h1>
    <p>Your bot is running on Render!</p>
    <p><a href="/set_webhook">📱 Set Webhook</a></p>
    <p><a href="/health">🩺 Health Check</a></p>
    <p><a href="/status">📊 Status</a></p>
    """

@app.route('/health')
def health():
    """Health check endpoint"""
    return 'OK', 200

@app.route('/status')
def status():
    """Bot status page"""
    import psutil
    memory = psutil.virtual_memory()
    
    return f"""
    <h2>🤖 Bot Status</h2>
    <p><strong>Status:</strong> 🟢 Online</p>
    <p><strong>Memory Usage:</strong> {memory.percent}%</p>
    <p><strong>Platform:</strong> Render.com</p>
    <p><strong>Commands Available:</strong> 15+</p>
    <p><a href="/">Home</a> | <a href="/set_webhook">Fix Webhook</a></p>
    """

@app.route('/set_webhook', methods=['GET'])
async def set_webhook():
    """Set webhook to current URL"""
    import asyncio
    
    current_url = request.host_url.rstrip('/')
    webhook_url = f"{current_url}/webhook"
    
    try:
        await application.bot.set_webhook(webhook_url)
        return f"""
        <h2>✅ Webhook Updated!</h2>
        <p><strong>New URL:</strong> {webhook_url}</p>
        <p><strong>Status:</strong> Webhook is now active!</p>
        <p><strong>Next Step:</strong> Send /start to your bot on Telegram!</p>
        <p><a href="/">Back to Home</a></p>
        """
    except Exception as e:
        return f"❌ Error setting webhook: {e}"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Receive updates from Telegram"""
    update = Update.de_json(request.get_json(force=True), application.bot)
    
    # Process update asynchronously
    async def process():
        await application.process_update(update)
    
    import asyncio
    asyncio.run(process())
    
    return 'OK', 200

# ==================== KEEP-ALIVE ====================

def start_keep_alive():
    """Background thread to keep Render from sleeping"""
    import threading
    import time
    
    def ping_server():
        while True:
            try:
                url = request.host_url.rstrip('/') if 'request' in locals() else os.environ.get('RENDER_EXTERNAL_URL', '')
                if url:
                    requests.get(f"{url}/health", timeout=5)
                    logger.info(f"Keep-alive ping sent at {datetime.datetime.now().strftime('%H:%M:%S')}")
            except:
                logger.warning("Keep-alive ping failed")
            time.sleep(240)  # 4 minutes
    
    thread = threading.Thread(target=ping_server, daemon=True)
    thread.start()
    logger.info("Keep-alive thread started")

# ==================== STARTUP ====================

if __name__ == '__main__':
    # Start keep-alive in background
    start_keep_alive()
    
    # Initialize bot (for polling - alternative to webhook)
    # application.run_polling()  # Don't use this with webhooks!
    
    # Start Flask server
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting bot server on port {port}")
    logger.info(f"🤖 Bot username: @{application.bot.username}")
    app.run(host='0.0.0.0', port=port)