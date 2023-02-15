from django.urls import path

from app.internal.transport.rest import handlers

urlpatterns = [path("me/<int:user_id>", handlers.me, name="me")]
