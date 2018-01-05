from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^select_un', 'SendQuery.views.select_un'),
    url(r'^select_cm', 'SendQuery.views.select_cm'),
    url(r'^select_cdma.do$', 'SendQuery.views.select_cdma'),
    url(r'^select_cdma1.do$', 'SendQuery.views.select_cdma1'),
    url(r'^select_auto_un', 'SendQuery.views.select_auto_un'),
    url(r'^select_auto_cm', 'SendQuery.views.select_auto_cm'),
    url(r'^select_auto_cdma', 'SendQuery.views.select_auto_cdma'),
)

