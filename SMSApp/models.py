from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid
from uuidfield import UUIDField
# Create your models here.
class SMSUser(AbstractUser):
  number = models.CharField(max_length=12, unique=False, blank=False, null=False)
  network = models.CharField(max_length=15, unique=False, blank=False, null=False)

class Message(models.Model):
  user = models.ForeignKey('SMSUser', default = None, blank=True, null=True)
  uuid = UUIDField(auto=True)  
  number = models.CharField(max_length=12, unique=False, blank=False, null=False)
  network = models.CharField(max_length=20, unique=False, blank=False, null=False)
  text = models.CharField(max_length=160, unique=False, blank=False, null=False)
  time = models.DateTimeField(auto_now=False, db_index=True, blank=False, null=False)
  created = models.DateTimeField(auto_now=True)
  sent = models.BooleanField(default = False)
  cancelled = models.BooleanField(default = False)

#Used to ignore messages sent to number
class BlackList(models.Model):
  number = models.CharField(max_length=12, unique=True, blank=False, null=False)

class Friends(models.Model):
    user = models.ForeignKey('SMSUser', related_name='user')
    friend = models.ForeignKey('SMSUser', related_name='friend')
  
