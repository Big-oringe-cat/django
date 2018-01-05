from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^insert_un', 'ServiceSmsInfo.views.insert_un'),
    url(r'^insert_cm', 'ServiceSmsInfo.views.insert_cm'),
    url(r'^insert_cdma.do', 'ServiceSmsInfo.views.insert_cdma'),
    url(r'^insert_cdma1.do', 'ServiceSmsInfo.views.insert_cdma1'),
)

