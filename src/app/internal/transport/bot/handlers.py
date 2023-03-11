import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.user_service import BotService
from app.internal.transport.service_user_entity import ServiceUserEntity
from app.internal.transport.bank_account_entity import BankAccountEntity

NO_PHONE_RESPONSE = "You have to set your phone number with /set_phone " \
                    "before using this command."


def generate_start_response():
    """Generates reply for /start handler"""
    available_commands = [
        ("/start", "View available commands."),
        ("/set_phone PHONE_NUMBER", "Set new phone number on your account."),
        ("/me", "Display your telegram account info."),
        ("/open_bank_account", "Register a bank account."),
        ("/issue_bank_card", "Register a bank card."),
        ("/account_info", "Display your account balance information."),
        ("/card_info", "Display your card account information."),
    ]
    text_back = [command + " - "
                 + value for [command, value] in available_commands]
    return "\n".join(text_back)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data and responds to the user"""
    # User data update
    user_entity = ServiceUserEntity.create_from_telegram_data(
        update.effective_user)
    await BotService.save_user(user_entity)
    # Response to user
    text_back = generate_start_response()
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_back)


def get_phone_number(text):
    """Takes Russian phone number from given string."""
    parsed_text = text.split()
    phone_number = parsed_text[-1]
    if len(parsed_text) > 2 or not phone_number.startswith("+79") \
            or len(phone_number) != 12 or not phone_number[1:].isdigit():
        return None
    return phone_number


async def set_phone_handler(update: Update,
                            context: ContextTypes.DEFAULT_TYPE):
    """This handler verifies phone_number, updates user info and responds to
    the user."""
    # Phone number verification
    phone_number = get_phone_number(update.message.text)
    if not phone_number:
        text_back = "Wrong format, example:\n/set_phone +79123123123"
        return await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text_back
        )
    # User data update and user's phone number saving
    user_entity = ServiceUserEntity.create_from_telegram_data(
        update.effective_user)
    user_entity.phone_number = phone_number
    await BotService.save_user(user_entity)
    # Response to user
    text_back = "Saved, now you able to use /me command."
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_back)


def update_user(telegram_data):
    """This method updates user data"""
    user_entity = ServiceUserEntity.create_from_telegram_data(telegram_data)
    await BotService.save_user(user_entity=user_entity)


def has_phone(telegram_data):
    """This method checks if the user has a phone number"""
    db_user_data = await BotService.get_user(user_id=telegram_data.id)
    user_entity = ServiceUserEntity.create_from_db_data(db_user_data)
    if not user_entity.phone_number:
        return False
    return True

    
async def me_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is not available
     to user and responds accordingly."""
    # Update user data
    update_user(update.effective_user)
    # Is this command available? Response depending on it
    if not command_available(update.effective_user):
        return await context.bot.send_message(chat_id=update.effective_chat.id,
                                              text=NO_PHONE_RESPONSE)

    user_entity = ServiceUserEntity.create_from_db_data(
        BotService.get_user(update.effective_user.id))
    text_back = "Your profile info:\n" + str(user_entity)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_back)


async def open_bank_account_handler(update: Update,
                                    content: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is available to
     user and responds if not, then checks if a bank account exists otherwise
     creates bank account, then responds to the user."""
    # User data update
    update_user(update.effective_user)
    # Is this command available? Response if not
    if not command_available(update.effective_user):
        return await content.bot.send_message(chat_id=update.effective_chat.id,
                                              text=NO_PHONE_RESPONSE)

    # Checking the existence of a bank account and response if account exist
    user_entity = ServiceUserEntity.create_from_telegram_data(
        update.effective_user)
    db_account_data = await BotService.get_bank_account(user_id=user_entity.id)
    if db_account_data:
        text_back = "You already have bank account. Use /account_info to " \
                    "check your account information."
        return await content.bot.send_message(chat_id=update.effective_chat.id,
                                              text=text_back)
    # Create a bank account
    await BotService.create_bank_account(user_id=user_entity.id)
    # Response to user
    text_back = "Bank account was opened. Use /account_info to check your " \
                "account information."
    await content.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_back)


async def account_info_handler(update: Update,
                               context: ContextTypes.DEFAULT_TYPE):
    """This handler updated user data, checks if this command is available to 
    user, gets current user bank account information and reply to the user."""
    # User data update
    update_user(update.effective_user)
    # Is the command /open_bank_account available?
    if not command_available(update.effective_user):
        text_back = "You have to set your phone number with /set_phone " \
                    "before using this command."
        return await content.bot.send_message(chat_id=update.effective_chat.id,
                                              text=text_back) 

    db_account_data = await BotService.get_account(
        user_id=update.effective_user.id)
    if not db_account_data:
        text_back = "You don't have bank account."
        return await context.bot.send_message(chat_id=update.effective_chat.id,
                                              text=text_back)
    account_entity = BankAccountEntity(db_account_data=db_account_data)

    text_back = "Your account balance is: " + str(account.balance)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text_back)


async def issue_bank_card(update: Update,
                          content: ContextTypes.DEFAULT_TYPE):
    """Pass user id to bank card create method, generate answer and reply
    to the user."""
    await content.bot.send_message(chat_id=update.effective_chat.id,
                                   text="issue_bank_card")


async def card_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pass message text to get_card_balance method in BotService,
    then text back to user.
    """
    card_balance = await BotService.get_card_balance(user_id=update.effective_user.id)
    if card_balance:
        text_back = "Your card balance is: " + card_balance
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
    text_back = "You don't have any card."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
