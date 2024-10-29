from django.db import models
from django.contrib.auth.hashers import make_password
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)


    def pass_save(self,*args,**kargs):
        self.password = make_password(self.password)
        super(User.self).save(*args,**kargs)