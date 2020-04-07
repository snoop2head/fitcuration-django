import os
from django.core.management.base import BaseCommand
from users.models import User

admin_username = os.environ.get("ADMIN_ID")
admin_scrt = os.environ.get("ADMIN_PW")


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=admin_username)
        if not admin:
            User.objects.create_superuser(admin_username, admin_username, admin_scrt)
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
