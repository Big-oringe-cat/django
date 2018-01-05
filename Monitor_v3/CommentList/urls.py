from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'CommentList.views.select'),
    url(r'^insert', 'CommentList.views.insert'),
    url(r'^update', 'CommentList.views.update'),
    url(r'^modify', 'CommentList.views.modify'),
)

