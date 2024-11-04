from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes

from config import BOT_TOKEN, SERVICES_ENABLED

app = ApplicationBuilder().token(BOT_TOKEN).build()
# Commands
COMMANDS = {

}

for command, handler in COMMANDS.items():
    app.add_handler(CommandHandler(command, handler))


for service in SERVICES_ENABLED:
    app.add_handler(MessageHandler(service.get_tg_filter(), service.tg_handler))


app.run_polling()
