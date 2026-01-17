from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8221663079:AAHR01BGwId6N4aL8HYu7yUwBK4n6eJ8Fng"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো 😄 আমি alive!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Bot is running...")
app.run_polling()
