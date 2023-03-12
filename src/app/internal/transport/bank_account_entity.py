from app.internal.transport.entity import Entity


class BankAccountEntity(Entity):
    id = None
    user_id = None
    balance = None

    @classmethod
    def create_from_db_data(cls, db_account_data):
        self = BankAccountEntity()
        self.id = db_account_data.id
        self.user_id = db_account_data.user_id
        self.balance = db_account_data.balance
        return self
