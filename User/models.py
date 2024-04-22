from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    Image = models.ImageField(upload_to='user_images', blank=True, null=True)
  

class Customer(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    street = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)


class Admin(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Task = models.CharField(max_length=15, blank=True, null=True)


class User_Phone_Num(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Phone_num = models.CharField(max_length=15, unique=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.User.username)

