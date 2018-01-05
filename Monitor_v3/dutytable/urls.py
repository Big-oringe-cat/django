from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^dutyedit','dutytable.views.dutyedit'),
    url(r'^dutyinsert','dutytable.views.dutyinsert'),
    url(r'^update','dutytable.views.update'),
    url(r'^delete','dutytable.views.delete'),
    url(r'^duty_table','dutytable.views.duty_table'),
    url(r'^dutyzhanshi','dutytable.views.dutyzhanshi'),
    url(r'^sendemail','dutytable.views.sendemail'),
    url(r'^dutyduty','dutytable.views.dutyduty'),

)
