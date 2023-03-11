import json

from django.http import HttpResponse

from app.internal.models.service_user import ServiceUser
from app.internal.models.card import Card
from app.internal.models.bank_account import BankAccount


class BotService:
    """Service for logical handling of data"""

    @staticmethod
    async def save_user(user_entity):
        """Grab and save user info in the database"""
        user_data_to_save = await BotService.get_user(user_entity.id)
        if not user_data_to_save:
            user_data_to_save = ServiceUser()

        user_data_to_save.id = user_entity.id
        user_data_to_save.username = user_entity.username
        user_data_to_save.first_name = user_entity.first_name
        user_data_to_save.last_name = user_entity.last_name
        user_data_to_save.language_code = user_entity.language_code
        if user_entity.phone_number:
            user_data_to_save.phone_number = user_entity.phone_number

        await user_data_to_save.asave()

    @staticmethod
    async def save_phone_number(user_id, phone_number):
        """Saves phone number of user with user_id.
        Returns True if phone saved, False otherwise.
        """
        db_user_data = await ServiceUser.objects.aget(id=user_id)
        db_user_data.phone_number = phone_number
        await db_user_data.asave()

    @staticmethod
    async def get_user(user_id):
        """Returns database user data if user with user_id found, None otherwise."""
        try:
            db_user_data = await ServiceUser.objects.aget(id=user_id)
        except ServiceUser.DoesNotExist:
            return None
        return db_user_data

    @staticmethod
    async def create_bank_account(user_id):
        """Creates new bank account on given user id."""
        account_id = (str(user_id) * 20)[:20]
        db_user_data = await BotService.get_user(user_id=user_id)
        bank_account_to_save = BankAccount(id=account_id, user=db_user_data)
        await bank_account_to_save.asave()

    @staticmethod
    async def get_bank_account(user_id):
        """Returns bank account entity if bank account with account_id found,
        None otherwise."""
        try:
            db_account_data = await BankAccount.objects.aget(user=user_id)
        except BankAccount.DoesNotExist:
            return None
        return db_account_data

    @staticmethod
    async def create_card(user_entity):
        pass

    @staticmethod
    async def get_card(card_id):
        """Returns card entity if card with card_id found, None otherwise."""
        try:
            db_card_data = await Card.objects.aget(id=card_id)
        except Card.DoesNotExist:
            return None
        return db_card_data


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
