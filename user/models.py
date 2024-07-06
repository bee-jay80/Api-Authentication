# from django.db import models
# from django.contrib.auth.models import  AbstractUser


# class User(AbstractUser):
#     name = models.CharField(max_length=55)
#     email = models.EmailField(max_length=255,unique=True,blank=False)
#     password = models.CharField(max_length=55)
#     username = None

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name