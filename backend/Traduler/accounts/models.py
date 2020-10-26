from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    gender = models.CharField(max_length=2)
    age = models.IntegerField(default=0)
    profile_image = models.TextField()
    introduce = models.TextField()