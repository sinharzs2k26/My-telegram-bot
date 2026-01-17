<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue" alt="Telegram">
  <img src="https://img.shields.io/badge/Hosted_on-Render-46a2f1" alt="Render">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Status-Online-brightgreen" alt="Status">
</p>

<h1 align="center">🤖 My Telegram Bot</h1>

<p align="center">
  A fully-featured Telegram bot hosted 100% free on Render.com with 15+ commands, API integrations, and 24/7 uptime.
</p>

<p align="center">
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-features">Features</a> •
  <a href="#-quick-deployment">Deploy</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-development">Development</a>
</p>

## 🚀 Live Demo

**Bot Username:** `@YourBotUsername` *(replace with yours)*

**Dashboard:** https://your-bot.onrender.com

## ✨ Features

### 🎯 Core Features
- ✅ **24/7 Uptime** - Never sleeps (thanks to keep-alive system)
- ✅ **Free Hosting** - Entirely on Render.com free tier
- ✅ **15+ Commands** - Rich command ecosystem
- ✅ **Smart Responses** - AI-like conversation
- ✅ **Auto-Deploy** - GitHub → Render CI/CD

### 🎭 Entertainment Commands
- `/joke` - Random jokes
- `/cat` - Cute cat pictures
- `/dog` - Adorable dog pictures
- `/quote` - Inspirational quotes
- `/roll` - Roll a dice (1-6)
- `/flip` - Flip a coin
- `/random` - Random number generator

### 🛠️ Utility Commands
- `/calc` - Simple calculator
- `/todo` - Personal to-do list
- `/weather` - Weather information
- `/time` - Current server time
- `/echo` - Echo your text
- `/about` - Bot information

## 🏗️ Architecture

```

📱 User's Telegram 
↓
☁️ Telegram Servers 
↓
🖥️ Render.com (Your Bot - Free Tier)
↓
⚡ Instant Response
↓
📱 Back to User

```

## 🚀 Quick Deployment

### 1. Prerequisites
- Telegram account
- GitHub account
- Render account (free)

### 2. Create Your Bot
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Choose name and username
4. Save your API token

### 3. Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Or manually:
```bash
# Clone and deploy
git clone https://github.com/yourusername/telegram-bot-render.git
cd telegram-bot-render
git push origin main

# Then on Render:
# 1. New Web Service
# 2. Connect GitHub repo
# 3. Add TELEGRAM_TOKEN environment variable
# 4. Deploy!
```

4. Set Up Webhook

After deployment, visit:

```
https://your-bot-name.onrender.com/set_webhook
```

5. Test Your Bot!

Send /start to your bot on Telegram!

📊 Commands Reference

Command Description Example
/start Welcome message /start
/help Show all commands /help
/joke Random joke /joke
/cat Cat picture /cat
/dog Dog picture /dog
/quote Inspirational quote /quote
/roll Roll dice (1-6) /roll
/flip Flip coin /flip
/random Random number /random 1 100
/weather Weather info /weather London
/calc Calculator /calc 2+2*3
/todo To-do list /todo add Buy milk
/time Server time /time
/echo Repeat text /echo Hello
/about Bot info /about

🛠️ Development

Local Setup

```bash
# Clone
git clone https://github.com/yourusername/telegram-bot-render.git
cd telegram-bot-render

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env
echo "TELEGRAM_TOKEN=your_token" > .env
echo "PORT=10000" >> .env

# Run
python bot.py
```

🔧 File Structure

```
telegram-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Dependencies
├── runtime.txt        # Python 3.11
├── render.yaml        # Render config
├── .gitignore        # Ignore rules
└── README.md         # This file
```

🌐 Web Dashboard

· Home: https://your-bot.onrender.com/
· Set Webhook: https://your-bot.onrender.com/set_webhook
· Health Check: https://your-bot.onrender.com/health

🔒 24/7 Uptime

· Internal Keep-Alive: Self-pinging every 4 minutes
· External Monitor: UptimeRobot (free, optional)
· Render Free Tier: 750 hours/month = 31 days

📄 License

MIT License - see LICENSE file.

🙏 Acknowledgments

· python-telegram-bot
· Render.com for free hosting
· TheCatAPI & DogCEO API

---

⭐ If you find this useful, please star the repo!

```

## **Key Fixes I Made:**

1. **Used `<p align="center">` with `<img>` tags** - HTML works in GitHub README
2. **Simplified badge URLs** - No complex query parameters
3. **Proper alignment** - Centered everything
4. **Working shields.io URLs** - Tested and verified