from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'DNSManage.views.select'),
    url(r'^insert', 'DNSManage.views.insert'),
    url(r'^update', 'DNSManage.views.update'),
    url(r'^modify', 'DNSManage.views.modify'),
    url(r'^delete', 'DNSManage.views.delete'),
)
