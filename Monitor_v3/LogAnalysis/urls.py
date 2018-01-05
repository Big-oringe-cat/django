from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^customerSubmit.do', 'LogAnalysis.views.customerSubmit'),
    url(r'^customerSpeed.do', 'LogAnalysis.views.customerSpeed'),
    url(r'^clusterSpeed.do', 'LogAnalysis.views.clusterSpeed'),
    url(r'^tdSend.do', 'LogAnalysis.views.tdSend'),
    url(r'^net_switch_mobile.do', 'LogAnalysis.views.net_switch_mobile'),
    url(r'^request_ip', 'LogAnalysis.views.request_ip'),
)

