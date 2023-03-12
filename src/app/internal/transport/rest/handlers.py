from app.internal.services.user_service import RestUserService


def me(request, user_id):
    response = RestUserService.me(user_id=user_id)
    return response
