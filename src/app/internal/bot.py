import logging
import os

from app.internal.transport.bot import handlers
from config.settings import BOT_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - " "%(message)s", level=logging.INFO)


def start_bot():
    """Adds handlers to application and start bot"""
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handlers.start_handler))
    application.add_handler(CommandHandler("set_phone", handlers.set_phone_handler))
    application.add_handler(CommandHandler("me", handlers.me_handler))
    application.add_handler(CommandHandler("open_bank_account", handlers.open_bank_account_handler))
    application.add_handler(CommandHandler("issue_bank_card", handlers.issue_bank_card_handler))
    application.add_handler(CommandHandler("account_info", handlers.account_info_handler))
    application.add_handler(CommandHandler("card_info", handlers.card_info_handler))

    application.run_polling()
