from SMSApp.models import *
from SMSApp.tasks import *
import uuid
import datetime
import time
from pytz import timezone
import pytz
from django.utils.timezone import utc


def queueMessage(user, number, msg, time, network):
    #Strip phone number of hypens (-) spaces(' ') and parentheses('()')
    phone = number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    #Get a datetime that is 30 minutes from now, Check if message time is within 30 minutes and if so queue it to tasks otherwise queue it to table
    future= datetime.datetime.now() + datetime.timedelta(minutes=30)
    print "--QUEUEMESSAGE---"
    print "now" + str(datetime.datetime.utcnow().replace(tzinfo=utc))
    print "future" + str(future)
    print "time" + str(time)

    if not user.is_authenticated():
        user = None

    msgQueue = Message.objects.create(
        user=user,
        number =number,
        network = network,
        text = msg,
        time = time)

    if time < future:
      #Send message to task queue now.
      #now=datetime.datetime.now()
      print time
      #local = pytz.timezone ("America/Chicago")
      #local = local.localize(time, is_dst=None)
      #time = local.astimezone(timezone('US/Eastern'))
      now = datetime.datetime.now()
      seconds = timestamp(time) - timestamp(now)
      print '-------------'
      #print local
      print time
      print now
      print seconds
      print '-------taskid----------'
      print msgQueue.id
      print '-----------------'
      email_Reminder.apply_async((msgQueue.id, msg,number,network), task_id=str(msgQueue.uuid), queue='celery', countdown=int(seconds))



