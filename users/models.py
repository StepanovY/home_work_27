from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class UserRoles:
    MEMBER = 'member'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    choises = ((MEMBER, 'Пользователь'), (ADMIN, 'Администратор'), (MODERATOR, 'Модератор'))


class User(AbstractUser):
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    last_name = models.TextField(verbose_name='Фамилия', max_length=100, null=True)
    username = models.CharField(verbose_name='Логин', max_length=100, unique=True)
    password = models.CharField(verbose_name='Пароль', max_length=100)
    role = models.CharField(choices=UserRoles.choises, default=UserRoles.MEMBER, max_length=10)
    age = models.PositiveIntegerField()
    location = models.ManyToManyField(Location)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
