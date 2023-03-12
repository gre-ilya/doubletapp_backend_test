import json

from django.http import HttpResponse

from app.internal.models.service_user import ServiceUser


class UserService:
    """Service for logical handling of data"""

    @staticmethod
    async def save_user(user_entity):
        """Grab and save user info in the database"""
        user_data_to_save = await UserService.get_user(user_entity.id)
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
    async def get_user(user_id):
        """Returns database user data if user with user_id found, None
        otherwise."""
        try:
            db_user_data = await ServiceUser.objects.aget(id=user_id)
        except ServiceUser.DoesNotExist:
            return None
        return db_user_data


class RestUserService:
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
