from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid
from uuidfield import UUIDField
# Create your models here.
class SMSUser(AbstractUser):
  number = models.CharField(max_length=10, unique=False, blank=False, null=False)
  network = models.CharField(max_length=15, unique=False, blank=False, null=False)
  messageCount = models.PositiveIntegerField()

#Storing information for most common
class PhoneNumber(models.Model):
  number = models.CharField(max_length=10, unique=True, blank=False, null=False)
  network = models.CharField(max_length=20, unique=False, blank=False, null=False)
  count = models.PositiveIntegerField()
  lastUsed = models.DateTimeField(auto_now=True)
  
class Message(models.Model):
  text = models.CharField(max_length=160, unique=True, blank=False, null=False)
  count = models.PositiveIntegerField()
    
class Time(models.Model):
  time = models.DateTimeField(unique=True, blank=False, null=False)
  count = models.PositiveIntegerField()

  

#Used to ignore messages sent to number
class BlackList(models.Model):
  number = models.CharField(max_length=10, unique=True, blank=False, null=False)

class MessageQueue(models.Model):
  uuid = UUIDField(auto=True)
  number = models.CharField(max_length=10, unique=False, blank=False, null=False)
  network = models.CharField(max_length=20, unique=False, blank=False, null=False)
  text = models.CharField(max_length=160, unique=False, blank=False, null=False)
  time = models.DateTimeField(auto_now=False, db_index=True, blank=False, null=False)

class UserMessageQueue(models.Model):
  user = models.ForeignKey('SMSUser')
  message = models.ForeignKey('MessageQueue')

  