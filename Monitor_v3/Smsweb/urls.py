from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^Smssubmit', 'Smsweb.views.Smssubmit'),
    url(r'^Smssend', 'Smsweb.views.Smssend'),
)
