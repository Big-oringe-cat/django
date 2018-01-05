from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^insert', 'AutoSendConfig.views.insert'),
    url(r'^select', 'AutoSendConfig.views.select'),
    url(r'^update', 'AutoSendConfig.views.update'),
    url(r'^modify', 'AutoSendConfig.views.modify'),
#    url(r'^delete', 'AutoSendConfig.views.delete'),
    url(r'^option', 'AutoSendConfig.views.option'),
)

