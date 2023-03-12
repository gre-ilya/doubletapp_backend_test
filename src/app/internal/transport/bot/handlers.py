import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.bank_account_service import BankAccountService
from app.internal.services.card_service import CardService
from app.internal.services.user_service import UserService
from app.internal.transport.bank_account_entity import BankAccountEntity
from app.internal.transport.bot.checker import Checker
from app.internal.transport.card_entity import CardEntity
from app.internal.transport.user_entity import UserEntity

NO_PHONE_RESPONSE = "You have to set your phone number with /set_phone " "before using this command."
NO_BANK_ACCOUNT_RESPONSE = "You have to create your bank account with " "/open_bank_account before using this command."
NO_CARD_RESPONSE = "You have to create your card with /issue_bank_card " "before using this command."


def generate_start_response():
    """Generates reply for /start handler"""
    available_commands = [
        ("/start", "View available commands."),
        ("/set_phone PHONE_NUMBER", "Set new phone number on your account."),
        ("/me", "Display your telegram account info."),
        ("/open_bank_account", "Register a bank account."),
        ("/account_info", "Display your account balance information."),
        ("/issue_bank_card", "Register a bank card."),
        ("/card_info", "Display your card account information."),
    ]
    text_back = [command + " - " + value for [command, value] in available_commands]
    return "\n".join(text_back)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data and responds to the user"""
    # User data update
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Response to user
    text_back = generate_start_response()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


def parse_get_phone_input(text):
    """Takes Russian phone number from given string."""
    parsed_text = text.split()
    phone_number = parsed_text[-1]
    if (
        len(parsed_text) > 2
        or not phone_number.startswith("+79")
        or len(phone_number) != 12
        or not phone_number[1:].isdigit()
    ):
        return None
    return phone_number


async def set_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler verifies phone_number, updates user info and responds to
    the user."""
    # Phone number verification
    phone_number = parse_get_phone_input(update.message.text)
    if not phone_number:
        text_back = "Wrong format, example:\n/set_phone +79123123123"
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
    # User data update and user's phone number saving
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    user_entity.phone_number = phone_number
    await UserService.save_user(user_entity)
    # Response to user
    text_back = "Saved, now you able to use /me command."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def me_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is not available
    to user and responds accordingly."""
    # Update user data
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Does the user have a phone number? Response if not
    user_entity = UserEntity.create_from_db_data(await UserService.get_user(user_entity.id))
    if not await Checker.user_has_phone(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_PHONE_RESPONSE)
    # Response to user
    text_back = "Your profile info:\n" + str(user_entity)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def open_bank_account_handler(update: Update, content: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is available to
    user and responds if not, then checks if a bank account exists and
    response if it is otherwise creates bank account, then responds to the
    user."""
    # User data update
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Does the user have a phone number and bank account? Response if not
    user_entity = UserEntity.create_from_db_data(await UserService.get_user(user_entity.id))
    if not await Checker.user_has_phone(user_entity):
        return await content.bot.send_message(chat_id=update.effective_chat.id, text=NO_PHONE_RESPONSE)
    # Does the user have a bank account? Response if yes
    if await Checker.user_has_bank_account(user_entity):
        text_back = "You already have bank account. Use /account_info to " "check your account information."
        return await content.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
    # Create a bank account
    await BankAccountService.create_bank_account(user_entity.id)
    # Response to user
    text_back = "Bank account was opened. Use /account_info to check your " "account information."
    await content.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def account_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updated user data, checks if this command is available to
    user, gets current user bank account information and reply to the user."""
    # User data update
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Does the user have a phone number? Response if not
    user_entity = UserEntity.create_from_db_data(await UserService.get_user(user_entity.id))
    if not await Checker.user_has_phone(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_PHONE_RESPONSE)
    # Does the user have a bank account? Response if not
    if not await Checker.user_has_bank_account(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_BANK_ACCOUNT_RESPONSE)
    # Response to user
    account_entity = BankAccountEntity.create_from_db_data(await BankAccountService.get_bank_account(user_entity.id))
    del account_entity.user_id
    text_back = "Your account info:\n" + str(account_entity)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def issue_bank_card_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is available to
    user, then checks if the card exists and response if yes, otherwise
    creates a new card and response to user."""
    # User data update
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Does the user have a phone number? Response if not
    if not await Checker.user_has_phone(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_PHONE_RESPONSE)
    # Does the user have a bank account? Response if not
    if not await Checker.user_has_bank_account(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_BANK_ACCOUNT_RESPONSE)
    # Does the user have a card? Response if yes
    if await Checker.has_card(user_entity):
        text_back = "You already have a card. Use /card_info to check your " "card information."
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
    # Create card
    user_entity = UserEntity.create_from_db_data(await UserService.get_user(user_entity.id))
    await CardService.create_card(user_id=user_entity.id, first_name=None, last_name=None)
    # Response to user
    text_back = "Card was issued. Use /card_info to check your card " "information"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)


async def card_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This handler updates user data, checks if this command is available to
    user, then checks if the card exists and response accordingly."""
    # User data update
    user_entity = UserEntity.create_from_telegram_data(update.effective_user)
    await UserService.save_user(user_entity)
    # Does the user have a phone number? Response if not
    if not await Checker.user_has_phone(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_PHONE_RESPONSE)
    # Does the user have a card? Response if not
    if not await Checker.has_card(user_entity):
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=NO_CARD_RESPONSE)
    # Response to user
    card_entity = CardEntity.create_from_db_data(await CardService.get_card(user_entity.id))
    account_entity = BankAccountEntity.create_from_db_data(await BankAccountService.get_bank_account(user_entity.id))
    card_entity.balance = account_entity.balance
    text_back = "Your card info is:\n" + str(card_entity)
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=text_back)
