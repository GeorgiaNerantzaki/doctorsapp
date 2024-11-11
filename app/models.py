from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length =100, null=True,blank=True, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email