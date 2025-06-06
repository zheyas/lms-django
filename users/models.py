
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # убираем стандартное поле username
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'   # главным логином делаем email
    REQUIRED_FIELDS = []       # дополнительные обязательные поля (оставляем пустым)

    def __str__(self):
        return self.email
