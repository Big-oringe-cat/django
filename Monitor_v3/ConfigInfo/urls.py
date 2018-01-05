from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'ConfigInfo.views.select'),
    url(r'^update', 'ConfigInfo.views.update'),
    url(r'^modify', 'ConfigInfo.views.modify'),
)

