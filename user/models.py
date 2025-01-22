from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password


# Create your models here.
class CustomUser(AbstractUser):
    author = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers")


    def save(self, *args, **kwargs):
        if self._state.adding and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


