from app.internal.models.bank_account import BankAccount
from app.internal.services.user_service import UserService


class BankAccountService:
    @staticmethod
    async def create_bank_account(user_id):
        """Creates new bank account on given user id."""
        account_id = (str(user_id) * 20)[:20]
        db_user_data = await UserService.get_user(user_id)
        bank_account_to_save = BankAccount(id=account_id, user=db_user_data)
        await bank_account_to_save.asave()

    @staticmethod
    async def get_bank_account(user_id):
        """Returns bank account entity if bank account with account_id found,
        None otherwise."""
        db_user_data = await UserService.get_user(user_id)
        if not db_user_data:
            return None
        try:
            db_account_data = await BankAccount.objects.aget(user=user_id)
        except BankAccount.DoesNotExist:
            return None
        return db_account_data
