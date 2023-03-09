import telegram.error
from multiprocessing import Process
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs the telegram bot with token from .env file."

    def handle(self, *args, **options):
        from app.internal.bot import start_bot

        try:
            start_bot()
        except telegram.error.InvalidToken:
            self.stdout.write(self.style.ERROR("Error. Bot has a bad token..."))
