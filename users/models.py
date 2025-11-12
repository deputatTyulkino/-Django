from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(verbose_name='Фото', blank=True, null=True, upload_to='users/%Y/%m/%d')
    birth = models.DateTimeField(verbose_name='Дата рождения', null=True, blank=True)
