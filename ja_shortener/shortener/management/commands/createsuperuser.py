from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Creates a superuser with the specified username, email and password'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the superuser')
        parser.add_argument('email', type=str, help='Email for the superuser')
        parser.add_argument('password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'User {username} already exists'))
                return

            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f'Email {email} is already in use'))
                return

            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created superuser {username}')
            )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Unexpected error: {str(e)}')
            ) 