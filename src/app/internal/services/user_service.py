import json

from django.http import HttpResponse

from app.internal.models.service_user import ServiceUser
from app.internal.models.card import Card
from app.internal.models.bank_account import BankAccount


class BotService:
    """Service for logical handling of data"""

    @staticmethod
    async def save_user(user_info):
        """Grab and save user info in the database"""
        try:
            tmp = await ServiceUser.objects.aget(id=user_info["id"])
        except ServiceUser.DoesNotExist:
            tmp = ServiceUser()

        update_db = False
        for i in user_info.keys():
            if user_info[i] != getattr(tmp, i):
                update_db = True
                setattr(tmp, i, user_info[i])
        if update_db:
            await tmp.asave()

        available_commands = [
            ("/start", "View available commands."),
            ("/set_phone [phone number]", "Set new phone number on your account."),
            ("/me", "View your account info. (Use /start for update)."),
            ("/card_balance [card number]", "View card balance."),
            ("/account_balance [account number]", "View account balance."),
        ]
        text_back = [command + " - " + value for [command, value] in available_commands]
        text_back = "\n".join(text_back)
        return text_back

    @staticmethod
    async def save_phone(user_id, message_text):
        """Get, verify and save mobile phone in the current user
        in the database. Now works only with Russian phone numbers.
        """
        parsed_text = message_text.split()
        phone = parsed_text[-1]
        if len(parsed_text) > 2 or not phone.startswith("+79") or len(phone) != 12 or not phone[1:].isdigit():
            return "Wrong format, example:\n /set_phone +79123123123"

        try:
            tmp = await ServiceUser.objects.aget(id=user_id)
        except ServiceUser.DoesNotExist:
            return "You have to use /start before using this command."
        tmp.phone_number = phone
        await tmp.asave()
        return "Saved, now you able to use /me command."

    @staticmethod
    async def get_user_info(user_id):
        """Returns information about user telegram account in key: value format"""
        try:
            tmp = await ServiceUser.objects.aget(id=user_id)
        except ServiceUser.DoesNotExist:
            return "You have to use /start before using this command."

        if not tmp.phone_number:
            return "You have to set your phone number with /set_phone before using this command."

        text_back = (
            "Your profile info:\n" + "\n".join([f"{i}: {getattr(tmp, i)}" for i in tmp]) + "\n"
            "Using /start automatically updates this information."
        )
        return text_back

    @staticmethod
    async def get_card_balance(message_text):
        parsed_text = message_text.split()
        card_number = parsed_text[-1]
        if len(parsed_text) != 2 or len(card_number) != 16 or not card_number.isdigit():
            return "Wrong card number. The card number is string of 16 digits."

        try:
            tmp = await Card.objects.aget(id=card_number)
        except Card.DoesNotExist:
            return "Card does not exist."
        return "Card balance is: " + str(tmp.balance)

    @staticmethod
    async def get_account_balance(message_text):
        parsed_text = message_text.split()
        account_number = parsed_text[-1]
        if len(parsed_text) != 2 or len(account_number) != 20 or not account_number.isdigit():
            return "Wrong account number. The account number is string of 20 digits."
        try:
            tmp = await BankAccount.objects.aget(id=account_number)
        except BankAccount.DoesNotExist:
            return "Account does not exist."
        return "Account balance is: " + str(tmp.balance)


class RestService:
    @staticmethod
    def me(user_id):
        user_data = {}
        try:
            tmp = ServiceUser.objects.get(id=user_id)
        except ServiceUser.DoesNotExist:
            return HttpResponse(json.dumps({}))

        for i in tmp:
            user_data[i] = getattr(tmp, i)
        response_json = json.dumps(user_data)
        return HttpResponse(response_json)
