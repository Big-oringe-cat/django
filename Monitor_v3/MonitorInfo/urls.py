from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'MonitorInfo.views.select'),
    url(r'^insert', 'MonitorInfo.views.insert'),
    url(r'^update$', 'MonitorInfo.views.update'),
    url(r'^updatenew$', 'MonitorInfo.views.updatenew'),
    url(r'^modify', 'MonitorInfo.views.modify'),
    url(r'^delete', 'MonitorInfo.views.delete'),
    url(r'^panduan','MonitorInfo.views.panduan'),
    url(r'^piliang','MonitorInfo.views.piliang'),
    url(r'^sqlxiugai','MonitorInfo.views.sqlxiugai'),
    url(r'^deal','MonitorInfo.views.deal'),
    url(r'^add_group','MonitorInfo.views.add_group'),
    url(r'^ServerConfig', 'MonitorInfo.views.ServerConfig'),
)

