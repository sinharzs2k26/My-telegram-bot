import os
import json
import logging
import threading
import time
import asyncio
import random
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from telegram import Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton
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

# ==================== COMMAND HANDLERS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start is issued"""
    user = update.effective_user
    
    welcome_text = f"""
👋 *Hello {user.first_name}!*

🤖 I'm your 24/7 Telegram bot hosted on *Render.com*!

📋 *Quick Access Commands:*
/start - Welcome message
/help - Show all commands
/ping - Check if I'm alive
/time - Current server time
/joke - Get a random joke
/cat - Get a random cat picture 🐱
/dog - Get a random dog picture 🐶
/quote - Inspirational quote
/roll - Roll a dice (1-6)
/flip - Flip a coin
/random - Random number generator
/weather - Weather information
/echo - Repeat your text
/about - About this bot
/calc - Simple calculator
/todo - To-do list manager

💡 *Try me!* Just send me any message and I'll respond!
    """
    
    # Create keyboard buttons
    keyboard = [
        [KeyboardButton("/help"), KeyboardButton("/time")],
        [KeyboardButton("/joke"), KeyboardButton("/cat")],
        [KeyboardButton("/dog"), KeyboardButton("/quote")],
        [KeyboardButton("/roll"), KeyboardButton("/flip")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)
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
/todo [add/list/clear] - To-do list

💡 *Tip:* You can just send me normal messages too!
I'll respond to greetings, questions, and more!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if bot is responsive"""
    await update.message.reply_text("🏓 *Pong!* I'm alive and running on Render! ⚡", parse_mode='Markdown')

async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send current server time"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    await update.message.reply_text(f"🕐 *Server Time:* `{current_time}`", parse_mode='Markdown')

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(f"😂 *Joke:* {joke}")

async def cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random cat picture"""
    try:
        # Using TheCatAPI
        response = requests.get("https://api.thecatapi.com/v1/images/search", timeout=5)
        if response.status_code == 200:
            cat_url = response.json()[0]['url']
            await update.message.reply_photo(photo=cat_url, caption="🐱 *Here's a cute cat for you!*", parse_mode='Markdown')
        else:
            await update.message.reply_text("😿 Couldn't fetch cat picture, try again later!")
    except Exception as e:
        logger.error(f"Cat API error: {e}")
        await update.message.reply_text("😿 Cat API is sleeping! Try /dog instead!")

async def dog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random dog picture"""
    try:
        response = requests.get("https://dog.ceo/api/breeds/image/random", timeout=5)
        if response.status_code == 200:
            dog_url = response.json()['message']
            await update.message.reply_photo(photo=dog_url, caption="🐶 *Here's a good doggo!*", parse_mode='Markdown')
        else:
            await update.message.reply_text("🐕 Couldn't fetch dog picture!")
    except Exception as e:
        logger.error(f"Dog API error: {e}")
        await update.message.reply_text("🐕 Dog API is busy! Try /cat instead!")

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(f"💭 *Quote:* {quote}")

async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll a dice"""
    result = random.randint(1, 6)
    await update.message.reply_text(f"🎲 *You rolled a {result}!*", parse_mode='Markdown')

async def flip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await update.message.reply_text(f"🪙 *It's {result}!*", parse_mode='Markdown')

async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate random number"""
    try:
        if context.args:
            if len(context.args) == 1:
                max_num = int(context.args[0])
                min_num = 1
            else:
                min_num = int(context.args[0])
                max_num = int(context.args[1])
            
            if min_num > max_num:
                min_num, max_num = max_num, min_num
                
            result = random.randint(min_num, max_num)
            await update.message.reply_text(f"🎯 *Random number between {min_num} and {max_num}:* `{result}`", 
                                          parse_mode='Markdown')
        else:
            # Default: 1-100
            result = random.randint(1, 100)
            await update.message.reply_text(f"🎯 *Random number (1-100):* `{result}`", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Please use numbers like: `/random 1 100` or `/random 50`", parse_mode='Markdown')

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get weather information"""
    if context.args:
        city = ' '.join(context.args)
        # Using OpenWeatherMap (would need API key)
        # For now, simulate response
        weather_types = ["☀️ Sunny", "🌧️ Rainy", "⛅ Cloudy", "❄️ Snowy", "🌪️ Windy", "⛈️ Stormy"]
        temp = random.randint(15, 35)
        weather = random.choice(weather_types)
        
        await update.message.reply_text(
            f"🌤️ *Weather for {city}:*\n"
            f"• Condition: {weather}\n"
            f"• Temperature: {temp}°C\n"
            f"• Humidity: {random.randint(40, 90)}%\n"
            f"• Wind: {random.randint(5, 25)} km/h\n\n"
            f"💡 *Note:* Add OpenWeatherMap API for real data!",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("🌍 *Usage:* `/weather [city]`\nExample: `/weather London`", parse_mode='Markdown')

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user's message"""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"📢 *You said:* `{text}`", parse_mode='Markdown')
    else:
        await update.message.reply_text("📢 *Usage:* `/echo [your text]`", parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information"""
    about_text = """
🤖 *About This Bot*

*Hosting:* Render.com (Free Tier)
*Uptime:* 24/7 with keep-alive
*Framework:* python-telegram-bot
*Version:* 2.0 (Fixed & Enhanced)

*Features:*
✅ 15+ commands
✅ Random jokes & quotes
✅ Cat/Dog pictures
✅ Calculator & utilities
✅ To-do list manager
✅ Smart message responses

*Status:* 🟢 Online and responsive
*Code:* GitHub + Render auto-deploy

This bot demonstrates how to host a feature-rich Telegram bot for free!
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple calculator"""
    if context.args:
        try:
            expression = ' '.join(context.args)
            # SECURITY: Basic validation
            allowed_chars = set('0123456789+-*/(). ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                await update.message.reply_text(f"🧮 *{expression} =* `{result}`", parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Only numbers and + - * / ( ) allowed!")
        except:
            await update.message.reply_text("❌ Invalid expression. Use: `/calc 2+2` or `/calc 10*5`", parse_mode='Markdown')
    else:
        await update.message.reply_text("🧮 *Usage:* `/calc [expression]`\nExample: `/calc (10+5)*2`", parse_mode='Markdown')

# Simple in-memory todo storage
user_todos = {}

async def todo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """To-do list manager"""
    user_id = update.effective_user.id
    
    if not context.args:
        # Show todo help
        help_text = """
📝 *To-Do List Manager*

*Commands:*
`/todo add [task]` - Add a new task
`/todo list` - Show all tasks
`/todo clear` - Clear all tasks
`/todo done [number]` - Mark task as done

*Examples:*
`/todo add Buy milk`
`/todo add Finish project`
`/todo list`
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
        return
    
    action = context.args[0].lower()
    
    if action == "add" and len(context.args) > 1:
        task = ' '.join(context.args[1:])
        if user_id not in user_todos:
            user_todos[user_id] = []
        user_todos[user_id].append(f"□ {task}")
        await update.message.reply_text(f"✅ *Added:* {task}", parse_mode='Markdown')
        
    elif action == "list":
        if user_id in user_todos and user_todos[user_id]:
            tasks = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_todos[user_id])])
            await update.message.reply_text(f"📝 *Your Tasks:*\n{tasks}", parse_mode='Markdown')
        else:
            await update.message.reply_text("📝 *Your to-do list is empty!*\nUse `/todo add [task]` to add tasks.", parse_mode='Markdown')
            
    elif action == "clear":
        user_todos[user_id] = []
        await update.message.reply_text("🗑️ *Cleared all tasks!*", parse_mode='Markdown')
        
    elif action == "done" and len(context.args) > 1:
        try:
            task_num = int(context.args[1]) - 1
            if user_id in user_todos and 0 <= task_num < len(user_todos[user_id]):
                task = user_todos[user_id].pop(task_num)
                await update.message.reply_text(f"✅ *Completed:* {task[2:]}", parse_mode='Markdown')
            else:
                await update.message.reply_text("❌ Invalid task number!")
        except ValueError:
            await update.message.reply_text("❌ Use: `/todo done [number]`", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Unknown action. Use: `/todo add/list/clear/done`", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages that are not commands"""
    user_message = update.message.text.lower()
    user = update.effective_user
    
    logger.info(f"Message from {user.id}: {user_message}")
    
    # Smart responses
    responses = {
        'hello': f"Hi {user.first_name}! 👋 How can I help you today?",
        'hi': f"Hello {user.first_name}! 😊",
        'hey': f"Hey there {user.first_name}!",
        'how are you': "I'm doing great, thanks for asking! Running smoothly on Render! ⚡",
        'thanks': "You're welcome! 😊",
        'thank you': "Anytime! Happy to help! 👍",
        'bye': "Goodbye! Have a great day! 👋",
        'goodbye': "See you later! 👋",
        'good morning': f"Good morning {user.first_name}! 🌅",
        'good night': "Good night! Sleep well! 🌙",
        'what is your name': "I'm your friendly Telegram bot hosted on Render! 🤖",
        'what can you do': "Type /help to see all my amazing commands! 📋",
        'who made you': "You created me! I'm your bot running 24/7 on Render! 🎉",
        'render': "Yes! I'm hosted for FREE on Render.com! 🚀",
        'python': "I'm built with Python and python-telegram-bot library! 🐍",
        'telegram': "Telegram is awesome for building bots! 💪",
        'cool': "Thanks! I think I'm pretty cool too! 😎",
        'awesome': "You're awesome too! ✨",
        'love you': "❤️ Aww, thanks! I'm just a bot, but I appreciate it!",
        'bot': "That's me! 🤖 How can I assist you?",
        'help': "Type /help for all commands, or just ask me anything!",
        'time': f"It's {datetime.now().strftime('%H:%M')}! Use /time for exact time.",
        'joke': "Sure! Try /joke for a random joke! 😂",
        'cat': "🐱 Meow! Use /cat for cute cat pictures!",
        'dog': "🐶 Woof! Use /dog for adorable dog pictures!",
        'weather': "🌤️ Use /weather [city] for weather information!",
    }
    
    # Check for matching responses
    for keyword, response in responses.items():
        if keyword in user_message:
            await update.message.reply_text(response)
            return
    
    # Default creative responses
    default_responses = [
        f"Interesting message, {user.first_name}! Try /help for all my features.",
        f"I received: '{update.message.text}' - Want to see what I can do? Type /help",
        f"Thanks for the message! Check out /help for all my commands!",
        f"Got it! Need assistance? I'm here to help! 🤖",
        f"👋 That's cool! Want a joke? Try /joke or a cat pic? Try /cat",
        f"Not sure how to respond to that! Try asking for /help or a /joke!",
    ]
    
    await update.message.reply_text(random.choice(default_responses))

# ==================== BOT INITIALIZATION ====================

def initialize_bot():
    """Initialize the Telegram bot application with ALL handlers"""
    global bot_application
    
    if not TOKEN:
        logger.error("❌ TELEGRAM_TOKEN environment variable is not set!")
        return None
    
    try:
        logger.info("🔄 Initializing Telegram bot with all features...")
        
        # Create bot application
        bot_application = Application.builder().token(TOKEN).build()
        
        # Register ALL command handlers
        bot_application.add_handler(CommandHandler("start", start_command))
        bot_application.add_handler(CommandHandler("help", help_command))
        bot_application.add_handler(CommandHandler("ping", ping_command))
        bot_application.add_handler(CommandHandler("time", time_command))
        bot_application.add_handler(CommandHandler("joke", joke_command))
        bot_application.add_handler(CommandHandler("cat", cat_command))
        bot_application.add_handler(CommandHandler("dog", dog_command))
        bot_application.add_handler(CommandHandler("quote", quote_command))
        bot_application.add_handler(CommandHandler("roll", roll_command))
        bot_application.add_handler(CommandHandler("flip", flip_command))
        bot_application.add_handler(CommandHandler("random", random_command))
        bot_application.add_handler(CommandHandler("weather", weather_command))
        bot_application.add_handler(CommandHandler("echo", echo_command))
        bot_application.add_handler(CommandHandler("about", about_command))
        bot_application.add_handler(CommandHandler("calc", calc_command))
        bot_application.add_handler(CommandHandler("todo", todo_command))
        
        # Register message handler for non-command messages
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ Bot initialized with 15+ commands and message handler")
        return bot_application
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {e}", exc_info=True)
        return None

# Initialize bot
bot_application = initialize_bot()

# ==================== FLASK ROUTES ====================

@app.route('/')
def home():
    """Home page dashboard"""
    bot_status = "✅ Online" if bot_application else "❌ Offline"
    command_count = 15 if bot_application else 0
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Feature-Rich Telegram Bot</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }}
            .container {{ max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ text-align: center; margin-bottom: 30px; }}
            .status-card {{ background: rgba(255,255,255,0.2); padding: 20px; border-radius: 15px; margin-bottom: 20px; }}
            .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }}
            .feature {{ background: rgba(255,255,255,0.15); padding: 15px; border-radius: 10px; text-align: center; }}
            .button {{ display: inline-block; background: #4CAF50; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin: 10px 5px; transition: transform 0.2s; }}
            .button:hover {{ transform: translateY(-2px); background: #45a049; }}
            .button.blue {{ background: #2196F3; }}
            .button.blue:hover {{ background: #1976D2; }}
            .command-list {{ background: rgba(0,0,0,0.2); padding: 20px; border-radius: 15px; margin-top: 20px; }}
            .command {{ display: inline-block; background: rgba(255,255,255,0.1); padding: 8px 15px; margin: 5px; border-radius: 20px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Feature-Rich Telegram Bot</h1>
            
            <div class="status-card">
                <h2>📊 Bot Status</h2>
                <p><strong>Status:</strong> {bot_status}</p>
                <p><strong>Commands:</strong> {command_count}+ features</p>
                <p><strong>Hosting:</strong> Render.com (Free Tier)</p>
                <p><strong>Uptime:</strong> 24/7 with keep-alive</p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="/set_webhook" class="button">🔗 SET WEBHOOK (DO THIS FIRST!)</a>
                <a href="/health" class="button blue">❤️ HEALTH CHECK</a>
                <a href="/bot_commands" class="button">📋 VIEW COMMANDS</a>
            </div>
            
            <div class="feature-grid">
                <div class="feature">🎭 Jokes</div>
                <div class="feature">🐱 Cat Pics</div>
                <div class="feature">🐶 Dog Pics</div>
                <div class="feature">💭 Quotes</div>
                <div class="feature">🎲 Games</div>
                <div class="feature">🧮 Calculator</div>
                <div class="feature">📝 To-Do List</div>
                <div class="feature">🌤️ Weather</div>
                <div class="feature">⏰ Time</div>
                <div class="feature">🤖 AI Responses</div>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                After setting webhook, send <code>/start</code> to your bot on Telegram!
            </p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy" if bot_application else "unhealthy",
        "bot_initialized": bool(bot_application),
        "timestamp": datetime.now().isoformat(),
        "features": 15,
        "host": "Render.com"
    }), 200 if bot_application else 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set webhook and bot commands"""
    try:
        if not bot_application:
            return "❌ Bot not initialized. Check TELEGRAM_TOKEN in Render environment.", 500
        
        current_url = request.host_url.rstrip('/')
        webhook_url = f"{current_url}/webhook"
        
        # Set webhook and commands using async
        async def setup_async():
            try:
                # Initialize and start bot
                await bot_application.initialize()
                await bot_application.start()
                
                # Set webhook
                await bot_application.bot.set_webhook(webhook_url)
                
                # Set bot commands menu (appears when user types /)
                commands = [
                    BotCommand("start", "Welcome message"),
                    BotCommand("help", "Show all commands"),
                    BotCommand("ping", "Check if bot is alive"),
                    BotCommand("time", "Current server time"),
                    BotCommand("joke", "Get a random joke"),
                    BotCommand("cat", "Get a random cat picture"),
                    BotCommand("dog", "Get a random dog picture"),
                    BotCommand("quote", "Inspirational quote"),
                    BotCommand("roll", "Roll a dice (1-6)"),
                    BotCommand("flip", "Flip a coin"),
                    BotCommand("random", "Random number generator"),
                    BotCommand("weather", "Weather information"),
                    BotCommand("echo", "Repeat your text"),
                    BotCommand("about", "About this bot"),
                    BotCommand("calc", "Simple calculator"),
                    BotCommand("todo", "To-do list manager"),
                ]
                await bot_application.bot.set_my_commands(commands)
                
                return True, "✅ Webhook and 16 commands set successfully!"
            except Exception as e:
                return False, f"❌ Error: {str(e)}"
        
        # Run async setup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success, message = loop.run_until_complete(setup_async())
        loop.close()
        
        if success:
            return f"""
            <!DOCTYPE html>
            <html>
            <head><title>✅ Success!</title><meta name="viewport" content="width=device-width, initial-scale=1">
            <style>body {{ font-family: Arial, sans-serif; margin: 40px; text-align: center; }}</style></head>
            <body>
                <h1>✅ Bot Setup Complete!</h1>
                <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <p><strong>Webhook URL:</strong><br><code>{webhook_url}</code></p>
                    <p><strong>Status:</strong> {message}</p>
                </div>
                <h3>🚀 Your bot now has:</h3>
                <ul style="text-align: left; display: inline-block;">
                    <li>16 Telegram menu commands</li>
                    <li>Random jokes & quotes</li>
                    <li>Cat & Dog pictures</li>
                    <li>Games (dice, coin flip)</li>
                    <li>Calculator & To-do list</li>
                    <li>Smart message responses</li>
                    <li>24/7 Render hosting</li>
                </ul>
                <p style="margin-top: 30px;">
                    <strong>Next Step:</strong> Send <code>/start</code> to your bot on Telegram!
                </p>
                <p><a href="/" style="color: #2196F3;">← Back to Dashboard</a></p>
            </body>
            </html>
            """
        else:
            return f"<h2>❌ Setup Failed</h2><pre>{message}</pre>", 500
            
    except Exception as e:
        logger.error(f"Error in set_webhook: {e}", exc_info=True)
        return f"<h2>❌ Error</h2><pre>{str(e)}</pre>", 500

@app.route('/bot_commands')
def bot_commands():
    """Show all available bot commands"""
    commands = [
        ("/start", "Welcome message with keyboard"),
        ("/help", "Show all available commands"),
        ("/ping", "Check if bot is alive"),
        ("/time", "Current server time"),
        ("/joke", "Get a random joke"),
        ("/cat", "Random cat picture from TheCatAPI"),
        ("/dog", "Random dog picture from DogCEO API"),
        ("/quote", "Inspirational quote"),
        ("/roll", "Roll a dice (1-6)"),
        ("/flip", "Flip a coin (Heads/Tails)"),
        ("/random", "Generate random number (1-100 or custom)"),
        ("/weather", "Weather information for any city"),
        ("/echo", "Repeat your text back to you"),
        ("/about", "About this bot and hosting"),
        ("/calc", "Simple calculator (+, -, *, /)"),
        ("/todo", "Personal to-do list manager"),
    ]
    
    html_commands = "\n".join([f'<div class="command"><strong>{cmd}</strong><br><small>{desc}</small></div>' for cmd, desc in commands])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>📋 Bot Commands</title><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .command {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #4CAF50; }}
        .command strong {{ color: #333; }}
        .command small {{ color: #666; display: block; margin-top: 5px; }}
    </style>
    </head>
    <body>
        <h1>📋 Available Bot Commands</h1>
        <p>Total: {len(commands)} commands</p>
        {html_commands}
        <p style="margin-top: 30px;"><a href="/">← Back to Dashboard</a></p>
    </body>
    </html>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Telegram webhook - BULLETPROOF VERSION"""
    try:
        if not bot_application:
            logger.error("Bot application not initialized")
            return "Bot not initialized", 500
        
        # Parse the update
        update_data = request.get_json(force=True)
        update_id = update_data.get('update_id', 'unknown')
        logger.info(f"📨 Received update: {update_id}")
        
        # Create update object
        update = Update.de_json(update_data, bot_application.bot)
        
        # Process update in background thread
        def process_update_in_thread(update_obj):
            """Process update in a separate thread"""
            try:
                # Create new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Process the update
                loop.run_until_complete(bot_application.process_update(update_obj))
                
                loop.close()
                logger.info(f"✅ Processed update {update_obj.update_id}")
                
            except Exception as e:
                logger.error(f"❌ Error processing update: {e}", exc_info=True)
        
        # Start processing in background thread
        thread = threading.Thread(target=process_update_in_thread, args=(update,))
        thread.daemon = True
        thread.start()
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}", exc_info=True)
        return 'ERROR', 500

# ==================== KEEP-ALIVE SYSTEM ====================

def start_keep_alive():
    """Keep Render from sleeping - ping every 4 minutes"""
    def ping_server():
        while True:
            try:
                # Try to get URL from environment or request context
                url = os.environ.get('RENDER_EXTERNAL_URL', '')
                if not url:
                    # Fallback to constructing from service name
                    service_name = os.environ.get('RENDER_SERVICE_NAME', '')
                    if service_name:
                        url = f"https://{service_name}.onrender.com"
                    else:
                        url = "http://localhost:10000"
                
                response = requests.get(f"{url}/health", timeout=10)
                logger.info(f"🔄 Keep-alive ping ({response.status_code}): {datetime.now().strftime('%H:%M:%S')}")
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
    logger.info("=" * 60)
    logger.info("🚀 FEATURE-RICH TELEGRAM BOT STARTING UP")
    logger.info(f"🔑 Token: {'✅ Set' if TOKEN else '❌ Missing'}")
    logger.info(f"🤖 Commands: 15+ features loaded")
    logger.info(f"🌐 Host: Render.com Free Tier")
    logger.info("=" * 60)
    
    # Start Flask server
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌍 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)