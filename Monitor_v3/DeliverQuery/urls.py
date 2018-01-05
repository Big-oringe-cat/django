from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^select_auto_un', 'DeliverQuery.views.select_auto_un'),
    url(r'^select_auto_cm', 'DeliverQuery.views.select_auto_cm'),
    url(r'^select_auto_cdma', 'DeliverQuery.views.select_auto_cdma'),
    url(r'^select_un', 'DeliverQuery.views.select_un'),
    url(r'^select_cm', 'DeliverQuery.views.select_cm'),
    url(r'^select_cdma.do$', 'DeliverQuery.views.select_cdma'),
    url(r'^select_cdma1.do$', 'DeliverQuery.views.select_cdma1'),
)

