from tropo import Tropo, Session
import uuid
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import F
from django.views.generic import TemplateView
from SMSApp.forms import *
from SMSApp.tasks import *
from SMSApp.models import *
from SMSApp.functions import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.http import Http404
#Reset PW
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm

#from django.core.mail import send_mail
from django.core.mail import EmailMessage
from dateutil.parser import *
from dateutil.tz import *
from time import mktime
from datetime import datetime
from celery.task.control import revoke
# import the logging library
import parsedatetime.parsedatetime as pdt
import logging
import requests

import time
# Get an instance of a logger
logger = logging.getLogger(__name__)
User = get_user_model()



def about(request):
    return HttpResponse("You're looking at about page")
def add_contact(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = BlockForm(request.POST) # A form bound to the POST data
        user = request.user
        if form.is_valid(): # All validation rules pass
            phone_number = form.cleaned_data['blacklist_phone_number']
            num = BlackList.objects.create(number=phone_number)
            messages.add_message(request, messages.INFO, 'The number has been successfully added to the blacklist.')
            return redirect('index')

        else:
            messages.add_message(request, messages.ERROR, 'Invalid phone number entered. Please try again.')
            return redirect('index')
    else:
        messages.add_message(request, messages.INFO, 'There was an issue with your request. Please try again.')
        return redirect('index')

def blocknumber_confirm(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = BlockForm(request.POST) # A form bound to the POST data
        user = request.user
        if form.is_valid(): # All validation rules pass
            phone_number = form.cleaned_data['blacklist_phone_number']
            num = BlackList.objects.create(number=phone_number)
            messages.add_message(request, messages.INFO, 'The number has been successfully added to the blacklist.')
            return redirect('index')

        else:
            messages.add_message(request, messages.ERROR, 'Invalid phone number entered. Please try again.')
            return redirect('index')
    else:
        messages.add_message(request, messages.INFO, 'There was an issue with your request. Please try again.')
        return redirect('index')


def blocknumber(request):
  form_class = BlockForm
  form = BlockForm() # An unbound form
  return render(request, 'SMSApp/sections/blocknumber.html', {'form': form})

def delete_messages(request):
  c = {}
  c.update(csrf(request))
  user = request.user
  if request.method == 'POST': # If the form has been submitted...
    for key, value in request.POST.iteritems():
      if value == "on":
        print '--------------DELETE MESSAGE------------'
        print key
        message = Message.objects.filter(uuid = key).update(cancelled=True)
        logger.info(message)
        revoke(str(key))
        #This doesnt seem to get called. TODO FIX

        #revoke_message(key)

    messages.add_message(request, messages.ERROR, 'The selected messages have been successfully cancelled!')
    return redirect('user_messages', user)
  else:
    messages.add_message(request, messages.ERROR, 'There was an error with your request. Please try again')
    return redirect('user_messages', user)
    

def faq(request):
  return render(request, 'SMSApp/faq.html')
  

def index(request):
    blacklistform = BlockForm()

    print "IP Address for debug-toolbar: " + request.META['REMOTE_ADDR']
    logger.error('TESTING!')
    if not request.user.is_authenticated():
        form = ReminderForm() # An unbound form
        logger.info('not auth!')
        return render(request, 'SMSApp/index.html', {
            'user': "",                                         
            'form': form,
            'blacklistform' : blacklistform
        })
    else:
      #request.user.first_name
      form = ReminderForm(initial={'phone_number': request.user.number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '') , 'network': request.user.network}) # An unbound form
      return render(request, 'SMSApp/index.html', {
            'user': request.user,
            'form': form,
            'blacklistform' : blacklistform
        })

def signout_confirm(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been successfully logged out.')
    return redirect('index')
  
def smsconfirm(request):
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = ReminderForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            #phone_number = request.POST['phone_number']
            #time = request.POST['date']
            #message = request.POST['message']

            phone_number = form.cleaned_data['phone_number']
            time = form.cleaned_data['date']
            usertime = form.cleaned_data['date2']
            message = form.cleaned_data['message']
            network = form.cleaned_data['network']
            
            #Do time conversion if needed.
            try:
              if parse(time):
                time = parse(time)
            except TypeError, ex:
                cal = pdt.Calendar()
                time = datetime.fromtimestamp(mktime(cal.parse(time)[0]))
            except ValueError, exVal:
                cal = pdt.Calendar()
                time = datetime.fromtimestamp(mktime(cal.parse(time)[0]))
                
            #Check if number is blacklisted
            if not BlackList.objects.filter(number=phone_number):
              queueMessage(request.user, phone_number, message, time, network)
              messages.add_message(request, messages.INFO, 'Your message has been created!')
              return redirect('index')

            else:
                messages.add_message(request, messages.ERROR, 'This number has been blacklisted.')
                return redirect('index')
        else:
            blacklistform = BlockForm()
            form = ReminderForm(request.POST) # An unbound form
            return render(request, 'SMSApp/index.html', {
            'user': request.user,
            'form': form,
            'blacklistform' : blacklistform
        })
    else:
        messages.add_message(request, messages.ERROR, 'There was an error with processing your request. Please try again.')
        return redirect('index')

def signin(request):
    signinform = SigninForm()
    return render(request, 'SMSApp/sections/signin.html', {
            'signinform' : signinform
        })

def signin_confirm(request):
  if request.method == 'POST': # If the form has been submitted...
          # ContactForm was defined in the the previous section
          form = SigninForm(request.POST) # A form bound to the POST data
          if form.is_valid(): # All validation rules pass
              user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
              remember = form.cleaned_data['remember']
              if user is not None:
                  # the password verified for the user
                  if user.is_active:
                       login(request, user)
                       if not remember:
                          logger.debug('NO REMEMBER!')
                          request.session.set_expiry(0)
                       else:
                          logger.debug('REMBER!')
                       messages.add_message(request, messages.INFO, 'You have been successfully signed in!')
                       return redirect('user_dashboard', request.user)
                       #return render(request, 'SMSApp/index.html', context)
                  else:
                    messages.add_message(request, messages.ERROR, 'We were unable to signin your account. It has been disabled.')
                    return redirect('signin')

              else:
                # the authentication system was unable to verify the username and password
                messages.add_message(request, messages.ERROR, 'We were unable to signin your account. Please check your username and password.')
                return redirect('signin')

          else:
            messages.add_message(request, messages.ERROR, 'There has been an error. Please check that you filled out the form correctly.')
            return redirect('signin')
  else:
      messages.add_message(request, messages.ERROR, 'There has been an error with the request. Please try again.')
      return redirect('signin')


def register(request):
    registerform = RegisterForm() # An unbound form
    context =  {'form': registerform}

    return render(request, 'SMSApp/sections/register.html', context)
  
def register_confirm(request):
  if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the the previous section
        form = RegisterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            logger.debug(phone_number)
            network = form.cleaned_data['network']

            user = User.objects.create(email=email, username=username, first_name=first_name, last_name=last_name, number=phone_number, network=network)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
              # the password verified for the user
              if user.is_active:
                login(request, user)
                messages.add_message(request, messages.INFO, 'You have been successfully registered.')
                return redirect('index')
              else:
                messages.add_message(request, messages.ERROR, 'We were unable to signin your account.')
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'We were unable to signin your account. Please check your username or password.')
                return redirect('index')
        else:
            registerform = RegisterForm(request.POST) # An unbound form
            context =  {'form': registerform}
            return render(request, 'SMSApp/sections/register.html', context)
            #messages.add_message(request, messages.ERROR, 'We were not able to register your account. Please check that you filled in the form correctly.')
            #return redirect('register')
  else:
    messages.add_message(request, messages.ERROR, 'There has been an error. Please try registering again.')
    return redirect('register')
def reset_sent(request):
    messages.add_message(request, messages.INFO, 'Your password reset request has been recieved. You should recieve a reset email shortly.')
    return redirect('signin')

def reset_success(request):
    messages.add_message(request, messages.INFO, 'Your password has been changed. You may now login.')
    return redirect('signin')

def reset_confirm(request, uidb64=None, token=None):
    form = ResetNewPasswordForm()
    return password_reset_confirm(request, template_name='SMSApp/sections/pwreset/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('reset_success'), extra_context={'form':form})


def reset(request):
    form = ResetPasswordForm()
    return password_reset(request, template_name='SMSApp/sections/pwreset/password_reset.html',
        email_template_name='SMSApp/sections/pwreset/password_reset_email.html',
        subject_template_name='SMSApp/sections/pwreset/password_reset_subject.txt',
        post_reset_redirect=reverse('reset_sent'), extra_context={'form':form})

def user_contacts(request, username):
    user = request.user
    if user.username == username:
        profile = get_object_or_404(SMSUser, username=username)
        form = AddContactForm()
        context = {'pagetype': 'contacts', 'profile':profile, 'form':form}
        return render(request, 'SMSApp/user/user.html', context)
    else:
        raise Http404

def user_dashboard(request, username):
    user = request.user
    if user.username == username:
        profile = get_object_or_404(SMSUser, username=username)
        form = ReminderForm()
        messages = Message.objects.all().filter(user=request.user, sent=False, cancelled = False)[:5]
        sentmessages = Message.objects.all().filter(user=request.user, sent=True, cancelled = False)[:5]
        context = {'pagetype': 'dashboard','form':form, 'profile':profile, 'sentmessages':sentmessages, 'messagequeue':messages}
        return render(request, 'SMSApp/user/user.html', context)
    else:
        raise Http404

def user_profile(request, username):
    user = request.user
    if user.username == username:
        profileForm = ProfileForm(initial={'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'phone_number':user.number, 'network':user.network}) # An unbound form
        profile = get_object_or_404(SMSUser, username=username)
        context = {'pagetype': 'profile', 'form': profileForm, 'profile':profile}
        return render(request, 'SMSApp/user/user.html', context)
    else:
        raise Http404

def user_messages(request, username):
  user = request.user
  if user.username == username:
    messages = Message.objects.all().filter(user=request.user, sent=False, cancelled = False)
    logger.info(messages.values())
    sentmessages = Message.objects.all().filter(user=request.user, sent=True, cancelled = False)
    logger.info(sentmessages.values())
    profile = get_object_or_404(SMSUser, username=username)
    context = {'pagetype': 'messages', 'sentmessages':sentmessages, 'messagequeue':messages, 'profile':profile}
    
    return render(request, 'SMSApp/user/user.html', context)
  else:
    raise Http404
def user_password(request,username):
  user = request.user
  if user.username == username:
    passwordForm = ChangePasswordForm()
    profile = get_object_or_404(SMSUser, username=username)
    context = {'pagetype': 'password', 'form': passwordForm, 'profile':profile}
    return render(request, 'SMSApp/user/user.html', context)
  else:
    raise Http404
def user_billing(request, username):
  user = request.user
  if user.username == username:
    profile = get_object_or_404(SMSUser, username=username)
    context = {'pagetype': 'billing', 'profile':profile}
    return render(request, 'SMSApp/user/user.html', context)
  else:
    raise Http404
def update_password(request):

  if request.method == 'POST': # If the form has been submitted...
          # ContactForm was defined in the the previous section
          form = ChangePasswordForm(request.POST) # A form bound to the POST data
          passwordForm = ChangePasswordForm()
          user = request.user
          if form.is_valid(): # All validation rules pass
              password = form.cleaned_data['password']
              new_password = form.cleaned_data['new_password']
              confirm_password = form.cleaned_data['confirm_password']
              user = authenticate(username=request.user, password=password)
              if new_password == confirm_password and user is not None:
                  # the password verified for the user
                  if user.is_active:
                      user = User.objects.get(id=request.user.id)
                      user.set_password(new_password)
                      user.save()
                      
                      messages.add_message(request, messages.INFO, 'Your new password has been successfully changed.')
                      return redirect('user_password', user)
                  else:
                      messages.add_message(request, messages.ERROR, 'There has been an error changing your password. Your account is currently disabled.')
                      return redirect('user_password', user)
              elif new_password != confirm_password:
                  messages.add_message(request, messages.ERROR, 'Your new and confirm passwords do not match.')
                  return redirect('user_password', user)
              else:
                  messages.add_message(request, messages.ERROR, 'Incorrect password. No changes have been made.')
                  return redirect('user_password', user)
          else:
              messages.add_message(request, messages.ERROR, 'Please verify that the information in the form is correctly entered.')
              return redirect('user_password', user)
  else:
      messages.add_message(request, messages.ERROR, 'There was an error with the request. Please try again.')
      return redirect('signin')

def update_profile(request):
  if request.method == 'POST': # If the form has been submitted...
    user = request.user
    form = ProfileForm(request.POST) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      email = form.cleaned_data['email']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      phone_number = form.cleaned_data['phone_number']
      network = form.cleaned_data['network']

      user = User.objects.get(id=request.user.id)
      user.email = email
      user.first_name = first_name
      user.last_name = last_name
      user.number = phone_number
      user.network = network
      user.save()
      messages.add_message(request, messages.INFO, 'Profile has been successfully updated.')
      return redirect('user_profile', user)
    else:
      messages.add_message(request, messages.ERROR, 'Please verify that the information in the form is correctly entered.')
      return redirect('user_profile', user)
  else:
      messages.add_message(request, messages.ERROR, 'There was an error with the request. Please try again.')
      return redirect('signin')