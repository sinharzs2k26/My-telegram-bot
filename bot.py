from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7786701907:AAEj2FwZnCfhYUQzm2BF65-IPmRaGsJVnRs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো 😄 আমি alive! (Bot by Saikat)")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443)

print("Bot is running...")
app.run_polling()