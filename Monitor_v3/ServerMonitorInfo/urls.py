from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'ServerMonitorInfo.views.select'),
    #url(r'^insert', 'ServerMonitorInfo.views.insert'),
    url(r'^update', 'ServerMonitorInfo.views.update'),
    url(r'^modify', 'ServerMonitorInfo.views.modify'),
    #url(r'^delete', 'ServerMonitorInfo.views.delete'),
)

