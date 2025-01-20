from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.
class CustomUser(AbstractUser):
    author = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(blank=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers")
    
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        """
        return make_password(value)

    def save(self, *args, **kwargs):
        # 새로운 사용자 생성 시 비밀번호 해시
        if self._state.adding and self.password:
            self.password = self.validate_password(self.password)
        super().save(*args, **kwargs)


