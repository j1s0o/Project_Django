from django.db import models
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver
from django.db.models.signals import pre_save

class Team(models.Model):
    name = models.CharField(max_length=55)
    password = models.CharField(max_length=32 )
    score = models.PositiveBigIntegerField(default=0)
    decription = models.CharField(max_length=100 , blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.name
    
    
class Chall(models.Model):
    list = (('Web exploit' , 'Web') , ('Cryptography', 'Crypto') , ('Pwnable','Pwn') , ('Reverse','Re'))
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
    team_solved = models.ManyToManyField(Team , null=True, blank=True)
    
    def __str__(self):
        return self.chall_name
    
class CustomUser(AbstractUser):
    solved = models.ManyToManyField(Chall , null=True , blank=True)
    score = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team, null=True, blank=True , on_delete= models.DO_NOTHING)
    def __str__(self):
        return self.username