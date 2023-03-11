from app.internal.transport.entity import Entity


class CardEntity(Entity):
    def __init__(self, db_card_data=None):
        self.id = db_card_data.id
        self.account_number = db_card_data.account_number
        self.expire_month = db_card_data.expire_month
        self.expire_year = db_card_data.expire_year
        self.owner_name = db_card_data.owner_name
        self.cvv = db_card_data.cvv
