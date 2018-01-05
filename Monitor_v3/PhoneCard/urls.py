from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^select_un', 'PhoneCard.views.select_un'),
    url(r'^select_cm', 'PhoneCard.views.select_cm'),
    url(r'^select_cdma.do$', 'PhoneCard.views.select_cdma'),
    url(r'^select_cdma1.do$', 'PhoneCard.views.select_cdma1'),
    url(r'^update_un', 'PhoneCard.views.update_un'),
    url(r'^update_cm', 'PhoneCard.views.update_cm'),
    url(r'^update_cdma$', 'PhoneCard.views.update_cdma'),
    url(r'^update_cdma1$', 'PhoneCard.views.update_cdma1'),
)

