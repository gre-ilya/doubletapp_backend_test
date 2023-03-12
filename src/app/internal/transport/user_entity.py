from app.internal.transport.entity import Entity


class UserEntity(Entity):
    id = None
    username = None
    first_name = None
    last_name = None
    language_code = None
    phone_number = None

    @classmethod
    def create_from_telegram_data(cls, telegram_user_data):
        telegram_user_data = telegram_user_data.to_dict()
        self = UserEntity()
        self.id = telegram_user_data['id']
        self.username = telegram_user_data.get('username', None)
        self.first_name = telegram_user_data.get('first_name', None)
        self.last_name = telegram_user_data.get('last_name', None)
        self.language_code = telegram_user_data.get('language_code', None)
        self.phone_number = telegram_user_data.get('phone_number', None)
        return self

    @classmethod
    def create_from_db_data(cls, db_user_data):
        self = UserEntity()
        self.id = db_user_data.id
        self.username = db_user_data.username
        self.first_name = db_user_data.first_name
        self.last_name = db_user_data.last_name
        self.language_code = db_user_data.language_code
        self.phone_number = db_user_data.phone_number
        return self
