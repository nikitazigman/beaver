from django.core.management.base import BaseCommand
from users.models import BeaverUser


class Command(BaseCommand):
    help = "Creates Admin User if it does not exist"

    def handle(self, *args, **options):
        user = BeaverUser.objects.create_superuser(
            username="django_superuser", password="SuperUser123!"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user created: {user.username}, SuperUser123!"
                " Don't forget to change the password!"
            )
        )
