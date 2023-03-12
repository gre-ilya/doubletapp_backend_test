from app.internal.services.bank_account_service import BankAccountService
from app.internal.models.card import Card


class CardService:
    @staticmethod
    async def create_card(user_id, first_name, last_name):
        """Creates new card on given user id."""
        card_id = (str(user_id) * 16)[:16]
        db_bank_account = await BankAccountService.get_bank_account(user_id)
        card_to_save = Card(
            id=card_id,
            account=db_bank_account,
            expire_month=2,
            expire_year=28,
            owner_name="vasya",
            cvv="123"
        )
        await card_to_save.asave()

    @staticmethod
    async def get_card(user_id):
        """Returns card entity if card with card_id found, None otherwise."""
        db_bank_account_data = \
            await BankAccountService.get_bank_account(user_id)
        if not db_bank_account_data:
            return None
        try:
            db_card_data = await Card.objects.aget(account=db_bank_account_data)
        except Card.DoesNotExist:
            return None
        return db_card_data
