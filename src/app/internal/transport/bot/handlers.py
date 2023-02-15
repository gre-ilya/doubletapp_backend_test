import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.user_service import BotService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pass user data as dict to the saving method in BotService,
    then text back to user.
    """
    user_info = update.effective_user.to_dict()
    text_back = await BotService.save_user(user_info=user_info)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pass user telegram id and message text to the phone saving method in
    BotService, then text back to user.
    """
    user_id = update.effective_user.id
    message_text = update.message.text.split()
    text_back = await BotService.save_phone(user_id=user_id, message_text=message_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pass user telegram id to the get user info method in BotService,
    then text back to user.
    """
    user_id = update.effective_user.id
    text_back = await BotService.get_user_info(user_id=user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
