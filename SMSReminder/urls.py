from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()
if settings.DEBUG:
    import debug_toolbar

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SMSReminder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^SMSApp/', include('SMSApp.urls')),
    url(r'^admin/', include(admin.site.urls)),
   # url(r'^__debug__/', include(debug_toolbar.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
