from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from decouple import config


class Command(BaseCommand):
    help = "Crea el superusuario si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = config("DJANGO_SUPERUSER_USERNAME")
        email = config("DJANGO_SUPERUSER_EMAIL")
        password = config("DJANGO_SUPERUSER_PASSWORD")

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("El superusuario ya existe.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Superusuario creado correctamente.")
        )