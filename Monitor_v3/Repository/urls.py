from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select','Repository.views.select'),
    url(r'^insert','Repository.views.insert'),
    url(r'^delete','Repository.views.delete'),
    url(r'^update','Repository.views.update'),
)
