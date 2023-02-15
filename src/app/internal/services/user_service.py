import json

from django.http import HttpResponse

from app.internal.models.service_user import ServiceUser


class BotService:
    """Service for logical handling of data"""

    @staticmethod
    async def save_user(user_info):
        """Grab and save user info in the database"""
        try:
            tmp = await ServiceUser.objects.aget(id=user_info["id"])
        except ServiceUser.DoesNotExist:
            tmp = ServiceUser()

        update_db = False
        for i in user_info.keys():
            if user_info[i] != getattr(tmp, i):
                update_db = True
            setattr(tmp, i, user_info[i])

        if update_db:
            await tmp.asave()

        text_back = "Hello. "
        if getattr(tmp, "phone_number"):
            text_back += "You able to use /me command."
        else:
            text_back += "Use /set_phone to add your phone number, example:\n" "/set_phone +79123123123"
        return text_back

    @staticmethod
    async def save_phone(user_id, message_text):
        """Get, verify and save mobile phone in the current user
        in the database. Now works only with Russian phone numbers.
        """
        phone = message_text[-1]
        if len(message_text) == 2 and phone.startswith("+79") and len(phone) == 12 and phone[1:].isdigit():
            try:
                tmp = await ServiceUser.objects.aget(id=user_id)
                tmp.phone_number = phone
                await tmp.asave()
                text_back = "Saved, now you able to use /me command."
            except ServiceUser.DoesNotExist:
                text_back = "First use /start command."
        else:
            text_back = "Wrong format, example:\n /set_phone +79123123123"
        return text_back

    @staticmethod
    async def get_user_info(user_id):
        """Returns information about user telegram account in key: value format"""
        text_back = ""
        try:
            tmp = await ServiceUser.objects.aget(id=user_id)
            if not tmp.phone_number:
                text_back = "You have to set your phone number with " "set_phone before using this command."
        except ServiceUser.DoesNotExist:
            text_back = "You have to use /start before using this command."

        if not text_back:
            text_back = (
                "Your profile info:\n" + "\n".join([f"{i}: {getattr(tmp, i)}" for i in tmp]) + "\n"
                "Using /start automatically updates this information."
            )
        return text_back


class RestService:
    @staticmethod
    def me(request, user_id):
        user_data = {}
        try:
            tmp = ServiceUser.objects.get(id=user_id)
            for i in tmp:
                user_data[i] = getattr(tmp, i)
        except ServiceUser.DoesNotExist:
            pass

        response_json = json.dumps(user_data)
        return HttpResponse(response_json)
