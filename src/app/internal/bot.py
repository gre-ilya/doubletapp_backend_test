import logging
import sys

import telegram.error
from telegram.ext import ApplicationBuilder, CommandHandler
from app.internal.transport.bot import handlers

TOKEN = "Your bot token here"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


def start_bot():
    """Add handlers to application and execute it, works only from manage.py shell"""
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("set_phone", handlers.set_phone))
    application.add_handler(CommandHandler("me", handlers.me))
    application.run_polling()
