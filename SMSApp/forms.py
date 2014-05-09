from django import forms
from django.core.exceptions import ValidationError
from localflavor.us.forms import USPhoneNumberField
from dateutil.parser import *
from dateutil.tz import *
from time import mktime
from datetime import datetime

import time
from pytz import timezone
import pytz
from django.utils.timezone import utc
import parsedatetime.parsedatetime as pdt



class ReminderForm(forms.Form):
    phone_number = USPhoneNumberField(required = True)
    date = forms.CharField(max_length=50, required = True)
    message = forms.CharField(max_length=80, required = True)
    network = forms.CharField(max_length=80, required = True)

    def clean(self):
        time = self.cleaned_data.get('date')
        error_messages = []
        typeError = False
        valueError = False
        try:
            if parse(time):
                time = parse(time)
        except TypeError, ex:
            print "type error"
            typeError = True
            cal = pdt.Calendar()
            time = datetime.fromtimestamp(mktime(cal.parse(time)[0]))

        except ValueError, exVal:
            print "value error"
            valueError = True
            cal = pdt.Calendar()
            time = datetime.fromtimestamp(mktime(cal.parse(time)[0]))
        except AttributeError:
            raise ValidationError("Please enter a valid time format.")

        now = datetime.now()
        seconds = timestamp(time) - timestamp(now)
        print seconds
        if typeError or valueError or seconds < 0:
            raise ValidationError("Please enter a valid time format.")

        return self.cleaned_data

def timestamp(date):
    try:
        return time.mktime(date.timetuple())
    except ValueError, exVal:
        raise ValidationError("Please enter a valid time format.")

class BlockForm(forms.Form):
    blacklist_phone_number = USPhoneNumberField()
    
class SigninForm(forms.Form):
    username = forms.CharField(max_length=20, required = True)
    password = forms.CharField(max_length=30, required = True)
    remember = forms.BooleanField(initial=False, required = False)
    
class RegisterForm(forms.Form):
    email = forms.EmailField(help_text='Please enter a valid email address', required = True)
    confirmemail = forms.EmailField(help_text='Please enter a valid email address', required = True)
    username = forms.CharField(max_length=40, required = True)
    password1 = forms.CharField(max_length=30, required = True)
    password2 = forms.CharField(max_length=30, required = True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = USPhoneNumberField()
    network = forms.CharField(max_length=80, required = True)
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        error_messages = []
        if (self.cleaned_data.get('email') != self.cleaned_data.get('confirmemail')):
            error_messages.append("Email addresses must match.")
            #raise ValidationError(
            #    "Email addresses must match."
            #)

        if not password2:
            #raise ValidationError("You must confirm your password")
            error_messages.append("You must confirm your password")
        if password1 != password2:
            error_messages.append("Your passwords do not match")
            #raise ValidationError("Your passwords do not match")
        if len(error_messages):
            raise ValidationError(error_messages)

        return self.cleaned_data

class ProfileForm(forms.Form):
    email = forms.EmailField(help_text='Please enter a valid email address', required = True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    phone_number = USPhoneNumberField()
    network = forms.CharField(max_length=80, required = True)
    
class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=30, required = True)
    new_password = forms.CharField(max_length=30, required = True)
    confirm_password = forms.CharField(max_length=30, required = True)

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(help_text='Please enter a valid email address', required = True)

class ResetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(max_length=30, required = True)
    new_password2 = forms.CharField(max_length=30, required = True)