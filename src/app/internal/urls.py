from app.internal.transport.rest import handlers
from django.urls import path

urlpatterns = [path("me/<int:user_id>", handlers.me, name="me")]
