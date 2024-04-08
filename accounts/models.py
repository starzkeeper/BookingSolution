from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=100)

    class Meta:
        verbose_name_plural = 'Пользователи'
