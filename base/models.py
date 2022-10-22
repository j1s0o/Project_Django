from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=55)
    password = models.CharField(max_length=32 )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.name

class Chall(models.Model):
    list = (('Web exploite' , 'Web') , ('Cryptography', 'Crypto') , ('Pwnable','Pwn') , ('Reverse','Re'))
    chall_id = models.IntegerField(blank = True , default= 1)
    chall_name = models.CharField(max_length=50)
    decription = models.TextField(null=True , blank=True)
    link = models.TextField(null=True , blank=True)
    type = models.CharField(max_length=20 ,choices=list)
    img = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=20 , blank=True)
    flag = models.CharField(max_length=255)
    point = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.chall_name

