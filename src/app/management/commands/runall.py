import os
from multiprocessing import Process
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Runs the django server and telegram bot."
    addrport = "127.0.0.1:8000"

    def add_arguments(self, parser):
        parser.add_argument("addrport", nargs="?", help="Optional ipaddr:port")
        parser.add_argument("--noreload", action="store_true", help="Starts server in no reload mode.")

    def handle(self, *args, **options):
        # This condition protects the bot from trying to restart with StatReloader (this leads to an error)
        if os.environ.get("RUN_MAIN") == "true":
            Process(target=call_command, daemon=True, args=("runbot",)).start()

        if options["addrport"]:
            self.addrport = options["addrport"]

        if options.get("noreload"):
            call_command("runserver", self.addrport, noreload=True)
        else:
            call_command("runserver", self.addrport)
