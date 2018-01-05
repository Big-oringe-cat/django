from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^insert', 'UserInfo.views.insert'),
    url(r'^select', 'UserInfo.views.select'),
    url(r'^modify', 'UserInfo.views.modify'),
    url(r'^update', 'UserInfo.views.update'),
)

