from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'ServerManager.views.select'),
    url(r'^room_select', 'ServerManager.views.room_select'),
    url(r'^insert', 'ServerManager.views.insert'),
    url(r'^update', 'ServerManager.views.update'),
    url(r'^room_update', 'ServerManager.views.room_update'),
    url(r'^modify', 'ServerManager.views.modify'),
    url(r'^room_modify', 'ServerManager.views.room_modify'),
    url(r'^delete', 'ServerManager.views.delete'),
    url(r'^agentic', 'ServerManager.views.agentic'),
    url(r'^changeserver', 'ServerManager.views.changeserver'),
    url(r'^serverinfomation', 'ServerManager.views.serverinfomation'),

)
