from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'HttpMonitor.views.select'),
    url(r'^insert', 'HttpMonitor.views.insert'),
    url(r'^update', 'HttpMonitor.views.update'),
    url(r'^modify', 'HttpMonitor.views.modify'),
)

