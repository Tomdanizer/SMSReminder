from django.conf.urls import patterns, url
from SMSApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = patterns('',
    # ex: /SMSApp/
    url(r'^$', views.index, name='index'),
    url(r'^submitsms/$', views.smsconfirm, name='smsconfirm'),
    url(r'^blocknumber_confirm/$', views.blocknumber_confirm, name='blacklist'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signin_confirm/$', views.signin_confirm, name='signin_confirm'),
    url(r'^signout/$', views.signout_confirm, name='signout'),
    url(r'^register_confirm/$', views.register_confirm, name='register'),
    url(r'^register/$', views.register, name='register'),
    url(r'^delete_messages/$', views.delete_messages, name='delete_messages'),
    url(r'^update_password/$', views.update_password, name='update_password'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),

    #PW Reset
    #url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_confirm, name='password_reset_confirm'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.reset_confirm, name='password_reset_confirm'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset/success/$', views.reset_success, name='reset_success'),
    url(r'^reset/set/$', views.reset_sent, name='reset_sent'),

    # ex: /SMSApp/blocknumber
    url(r'^blocknumber/$', views.blocknumber, name='blocknumber'),
    # ex: /SMSApp/username/
    url(r'^profile/(?P<username>\w+)/$', views.user_profile, name='user_profile'),
    url(r'^messages/(?P<username>\w+)/$', views.user_messages, name='user_messages'),
    url(r'^password/(?P<username>\w+)/$', views.user_password, name='user_password'),
    url(r'^billing/(?P<username>\w+)/$', views.user_billing, name='user_billing'),

    
    # ex: /SMSApp/faq/


    # ex: /SMSApp/register

)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)