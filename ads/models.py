from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=1000)
    author = models.CharField(max_length=1000)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    is_published = models.BooleanField(default=True)


class Category(models.Model):
    name = models.CharField(max_length=1000, unique=True)

