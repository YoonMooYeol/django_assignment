from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    author = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers")
