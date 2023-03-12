from app.internal.services.user_service import UserService
from app.internal.services.card_service import CardService
from app.internal.services.bank_account_service import BankAccountService
from app.internal.transport.user_entity import UserEntity


class Checker:
    @staticmethod
    async def user_has_phone(user_entity):
        """This method checks if the database has user phone number."""
        db_user_data = await UserService.get_user(user_entity.id)
        user_entity = UserEntity.create_from_db_data(db_user_data)
        if user_entity.phone_number:
            return True
        return False

    @staticmethod
    async def user_has_bank_account(user_entity):
        """This method checks if user owns the bank account."""
        db_account_data = \
            await BankAccountService.get_bank_account(user_entity.id)
        if db_account_data:
            return True
        return False

    @staticmethod
    async def has_card(user_entity):
        """This method checks if user own card."""
        db_card_info = await CardService.get_card(user_entity.id)
        if db_card_info:
            return True
        return False
