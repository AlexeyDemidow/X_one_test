import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from users.models import CustomUser
from links.models import UserLink

from faker import Faker

fake = Faker()

link_types = ['website', 'book', 'article', 'music', 'video']
ids = []

for i in CustomUser.objects.all().values('id'):
    ids.append(i['id'])

for _ in range(1000):
    UserLink.objects.create(
        user_id=random.choice(ids),
        title=fake.company(),
        description=fake.text(),
        url=fake.uri(),
        link_type=random.choice(link_types)
    )
