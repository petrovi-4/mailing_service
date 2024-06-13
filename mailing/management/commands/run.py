from django.core.management import BaseCommand
from mailing.cron import send_email


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_email()
