import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler
from app.internal.transport.bot import handlers
from config.settings import BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def start_bot():
    """Add handlers to application and execute it, works only from manage.py shell
    >>from app.internal.bot import start_bot
    >>start_bot()
    Don't forget to set your token.
    """
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("set_phone", handlers.set_phone))
    application.add_handler(CommandHandler("me", handlers.me))
    application.add_handler(CommandHandler("card_balance", handlers.card_balance))
    application.add_handler(CommandHandler("account_balance", handlers.account_balance))

    application.run_polling()
