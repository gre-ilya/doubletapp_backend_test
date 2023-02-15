from app.internal.services.user_service import RestService


def me(request, user_id):
    response = RestService.me(request=request, user_id=user_id)
    return response
