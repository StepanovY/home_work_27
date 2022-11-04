from django.db import models

from ads.models import Ad
from users.models import User


class Selection(models.Model):
    name = models.CharField(max_length=200, unique=True)
    ads = models.ManyToManyField(Ad)
    author = models.ForeignKey(User, verbose_name='Автор', related_name='ad',
                               on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
