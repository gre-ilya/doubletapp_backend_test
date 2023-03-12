from app.internal.transport.entity import Entity


class CardEntity(Entity):
    id = None
    account_id = None
    expire_month = None
    expire_year = None
    owner_name = None
    cvv = None

    @classmethod
    def create_from_db_data(cls, db_card_data):
        self = CardEntity()
        self.id = db_card_data.id
        self.account_id = db_card_data.account_id
        self.expire_month = db_card_data.expire_month
        self.expire_year = db_card_data.expire_year
        self.owner_name = db_card_data.owner_name
        self.cvv = db_card_data.cvv
        return self
