from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^CommandQuery.do', 'CommandQuery.views.CommandQuery'),
    url(r'^clusterSubmit.do', 'CommandQuery.views.clusterSubmit'),
    url(r'^clusterSend.do', 'CommandQuery.views.clusterSend'),
    url(r'^clusterSpeed', 'CommandQuery.views.clusterSpeed'),
    url(r'^request_ip', 'CommandQuery.views.request_ip'),
    url(r'^usepro', 'CommandQuery.views.usepro'),
)

