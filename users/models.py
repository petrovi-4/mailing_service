from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name='номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    username = None
    email = models.EmailField(verbose_name='электронная почта', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    users_status = models.BooleanField(default=True, verbose_name='статус пользователя')

    class Meta:
        permissions = [
            ('change_user_status', 'Can change user status')
        ]
