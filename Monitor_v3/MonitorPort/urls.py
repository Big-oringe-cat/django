from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'MonitorPort.views.select'),
    url(r'^insert', 'MonitorPort.views.insert'),
    url(r'^update', 'MonitorPort.views.update'),
    url(r'^modify', 'MonitorPort.views.modify'),
)

