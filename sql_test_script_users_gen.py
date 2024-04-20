import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from users.models import CustomUser

from faker import Faker

fake = Faker()

for i in range(100):
    CustomUser.objects.create_user(
        email=fake.email(),
        password=f'password{i}'
    )
