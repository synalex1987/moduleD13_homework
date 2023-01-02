from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    # По умолчанию пользователь не активирован(нужно ввести код из почты)
    enabled = models.BooleanField(default = False)