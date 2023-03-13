import json

from django.http import HttpResponse

from app.internal.services.user_service import UserService
from app.internal.transport.checker import Checker
from app.internal.transport.user_entity import UserEntity


async def me(request, user_id):
    """Returns http response with user data in JSON format. If user don't
    exist returns {}"""
    db_user_data = await UserService.get_user(user_id)
    if not db_user_data:
        return HttpResponse(json.dumps({}))
    user_entity = UserEntity.create_from_db_data(db_user_data)
    if not await Checker.user_has_phone(user_entity):
        return HttpResponse(json.dumps({"phone_number": user_entity.phone_number}))
    response_data = {
        "telegram_id": user_entity.id,
        "username": user_entity.username,
        "first_name": user_entity.first_name,
        "last_name": user_entity.last_name,
        "language_code": user_entity.language_code,
        "phone_number": user_entity.phone_number,
    }
    return HttpResponse(json.dumps(response_data))
