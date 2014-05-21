from __future__ import absolute_import
from celery.task.control import revoke
from celery import *
from celery.task import periodic_task
from celery.task.schedules import crontab
from django.core.mail import EmailMessage
from SMSApp.models import *
import datetime
import time
import logging
import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)

@periodic_task(run_every=crontab(minute="*/30"))
def getQueueMessage():
    print 'getting queue messages'
    now=datetime.datetime.now()
    #Get all messages within the next 30minutes
    messages = Message.objects.all().filter(time__range=(datetime.datetime.now(),datetime.datetime.now() + datetime.timedelta(minutes=30)))
    for message in messages:
      print(timestamp(now) - timestamp(message.time))
      print message.text
      print message.number
      print message.network
      seconds = timestamp(now) - timestamp(message.time)
      print seconds


      email_Reminder.apply_async((message.id, message.text,message.number,message.network), task_id=str(message.uuid), queue='celery', countdown=int(seconds))
      


def timestamp(date):
    return time.mktime(date.timetuple())

@shared_task
def revoke_message(id):
    print "REVOKE"
    logger.debug(id)
    revoke(str(id), terminate=True)

@shared_task
def email_Reminder(id, msg, phone, network):
    print '---------EMAIL REMINDER DEBUG---------------'
    phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    if not network:
        email = EmailMessage('SMSReminder', msg, to=[phone+'@txt.att.net'])
    else:
        email = EmailMessage('SMSReminder', msg, to=[phone + '@' + network])
    email.send()
    print id

    print Message.objects.filter(id = id).update(sent=True)
    # message2 = Message.objects.filter(id = message)
    # #usermsg = Message.objects.filter(id = message.message.id).update(sent=True)
    #
    # print message
    # print message.values()
    # print '---mesage2---'
    # print message2.values()
    # message2.update(sent=True)
    # message2.save()
    #message.delete()
    