from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'ServerInfo.views.select'),
    url(r'^insert', 'ServerInfo.views.insert'),
    url(r'^update', 'ServerInfo.views.update'),
    url(r'^modify', 'ServerInfo.views.modify'),
    #url(r'^delete', 'ServerInfo.views.delete'),
    url(r'^CommandConfig', 'ServerInfo.views.CommandConfig'),
)

