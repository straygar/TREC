from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from main.views import uploadRun

#class MyRegistrationView(RegistrationView):
    #def get_success_url(self,request, user):
        #return '/rango/'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/',include('registration.backends.simple.urls')),
    url(r'^run/new/', uploadRun, name="new_run"),
    url(r'^captcha/', include('captcha.urls')),
)