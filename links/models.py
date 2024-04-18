from PIL import Image
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class UserLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    url = models.URLField(max_length=100)
    image = models.ImageField(default='static/default.png', upload_to='static/linkpics/')
    link_type = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)
    change_date = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.change_date = timezone.now()
        super().save(*args, **kwargs)
        if not self.image:
            self.image = 'static/default.png'
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title


class UserLinkCollection(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_links = models.ManyToManyField(UserLink, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True)
    change_date = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.change_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
