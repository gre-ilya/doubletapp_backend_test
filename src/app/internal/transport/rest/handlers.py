import json

from django.http import HttpResponse

from app.internal.services.user_service import UserService
from app.internal.transport.user_entity import UserEntity


async def me(request, user_id):
    """Returns an http response with user data in JSON format. If user don't
    exist returns {}"""
    db_user_data = await UserService.get_user(user_id)
    if not db_user_data:
        return HttpResponse(json.dumps({}))
    user_entity = UserEntity.create_from_db_data(db_user_data)
    return HttpResponse(json.dumps(dict(vars(user_entity))))
