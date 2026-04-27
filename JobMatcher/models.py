from django.db import models
from django.utils import timezone



# Create your models here.
class userlogin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, null=True)
    password = models.CharField(max_length=100)
    confirmpassword = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
class Resume(models.Model):
    user = models.CharField(max_length=200)
    details = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
class CoverLetter(models.Model):
    user = models.CharField(max_length=200)
    details= models.TextField()
    ccreated_at = models.DateTimeField(default=timezone.now)
    
class tb_login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
   