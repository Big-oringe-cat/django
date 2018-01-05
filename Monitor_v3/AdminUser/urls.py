from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'AdminUser.views.select'),
    url(r'^insert', 'AdminUser.views.insert'),
    url(r'^update', 'AdminUser.views.update'),
    url(r'^modify', 'AdminUser.views.modify'),
)

