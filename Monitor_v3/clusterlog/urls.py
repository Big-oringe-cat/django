from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^HttpLog', 'clusterlog.views.HttpLog'),
    url(r'^CmppLog', 'clusterlog.views.CmppLog'),
    url(r'^SmgpLog', 'clusterlog.views.SmgpLog'),
    url(r'^SgipLog', 'clusterlog.views.SgipLog'),
)
