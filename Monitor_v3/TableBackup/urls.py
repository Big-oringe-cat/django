from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'TableBackup.views.select'),
    url(r'^insert', 'TableBackup.views.insert'),
    url(r'^update', 'TableBackup.views.update'),
    url(r'^modify', 'TableBackup.views.modify'),
    url(r'^delete', 'TableBackup.views.delete'),
)

