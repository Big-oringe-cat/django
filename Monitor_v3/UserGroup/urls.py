from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'UserGroup.views.select'),
    url(r'^insert', 'UserGroup.views.insert'),
    url(r'^modify', 'UserGroup.views.modify'),
    url(r'^update', 'UserGroup.views.update'),
)

