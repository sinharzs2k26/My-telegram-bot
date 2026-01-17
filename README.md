# 🤖 Telegram Bot - 24/7 Free Hosting

A fully-featured Telegram bot hosted 100% free on Render.com with 15+ commands, API integrations, and 24/7 uptime.

<p align="center">
  <img src="https://img.shields.io/badge/Status-Online-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python">
  <img src="https://img.shields.io/badge/Telegram-Bot-blue" alt="Telegram">
  <img src="https://img.shields.io/badge/Hosted_on-Render-46a2f1" alt="Render">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## 🚀 Live Demo

**Bot Username:** [@YourBotUsername](https://t.me/YourBotUsername)  
**Dashboard:** [https://your-bot.onrender.com](https://your-bot.onrender.com)

## ✨ Features

<table>
  <tr>
    <td>✅ 24/7 Uptime</td>
    <td>✅ Free Hosting</td>
    <td>✅ 15+ Commands</td>
  </tr>
  <tr>
    <td>✅ Smart Responses</td>
    <td>✅ Auto-Deploy</td>
    <td>✅ Cat/Dog Pics</td>
  </tr>
  <tr>
    <td>✅ Jokes & Quotes</td>
    <td>✅ Calculator</td>
    <td>✅ To-Do List</td>
  </tr>
</table>

## 📊 Commands Reference

<table>
  <tr>
    <th width="150">Command</th>
    <th>Description</th>
    <th width="150">Example</th>
  </tr>
  <tr>
    <td><code>/start</code></td>
    <td>Welcome message with keyboard</td>
    <td><code>/start</code></td>
  </tr>
  <tr>
    <td><code>/help</code></td>
    <td>Show all commands</td>
    <td><code>/help</code></td>
  </tr>
  <tr>
    <td><code>/joke</code></td>
    <td>Get a random joke</td>
    <td><code>/joke</code></td>
  </tr>
  <tr>
    <td><code>/cat</code></td>
    <td>Random cat picture</td>
    <td><code>/cat</code></td>
  </tr>
  <tr>
    <td><code>/dog</code></td>
    <td>Random dog picture</td>
    <td><code>/dog</code></td>
  </tr>
  <tr>
    <td><code>/quote</code></td>
    <td>Inspirational quote</td>
    <td><code>/quote</code></td>
  </tr>
  <tr>
    <td><code>/roll</code></td>
    <td>Roll a dice (1-6)</td>
    <td><code>/roll</code></td>
  </tr>
  <tr>
    <td><code>/flip</code></td>
    <td>Flip a coin</td>
    <td><code>/flip</code></td>
  </tr>
  <tr>
    <td><code>/random</code></td>
    <td>Random number generator</td>
    <td><code>/random 1 100</code></td>
  </tr>
  <tr>
    <td><code>/weather</code></td>
    <td>Weather information</td>
    <td><code>/weather London</code></td>
  </tr>
  <tr>
    <td><code>/calc</code></td>
    <td>Simple calculator</td>
    <td><code>/calc 2+2*3</code></td>
  </tr>
  <tr>
    <td><code>/todo</code></td>
    <td>To-do list manager</td>
    <td><code>/todo add Buy milk</code></td>
  </tr>
  <tr>
    <td><code>/time</code></td>
    <td>Current server time</td>
    <td><code>/time</code></td>
  </tr>
  <tr>
    <td><code>/echo</code></td>
    <td>Repeat your text</td>
    <td><code>/echo Hello World</code></td>
  </tr>
  <tr>
    <td><code>/about</code></td>
    <td>Bot information</td>
    <td><code>/about</code></td>
  </tr>
</table>

## 🚀 Quick Deployment

### 1. Create Your Bot
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Choose name and username
4. Save your API token

### 2. Deploy on Render
```bash
# Clone repository
git clone https://github.com/yourusername/telegram-bot-render.git
cd telegram-bot-render

# Deploy on Render:
# 1. Go to render.com
# 2. Click "New +" → "Web Service"
# 3. Connect your GitHub repo
# 4. Configure as shown above
# 5. Add TELEGRAM_TOKEN environment variable