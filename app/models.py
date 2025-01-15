from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length =100, null=True,blank=True, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email



class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"