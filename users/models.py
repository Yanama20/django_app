from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='users_avatar/', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
