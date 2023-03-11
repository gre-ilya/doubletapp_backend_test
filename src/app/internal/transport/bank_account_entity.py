from app.internal.transport.entity import Entity


class BankAccountEntity(Entity):
    def __init__(self, db_account_data=None):
        self.id = db_account_data.id
        self.user_id = db_account_data.user_id
        self.balance = db_account_data.balance
