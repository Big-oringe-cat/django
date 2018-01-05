from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^insert_un', 'OutBox.views.insert_un'),
    url(r'^insert_cm', 'OutBox.views.insert_cm'),
    url(r'^insert_cdma.do$', 'OutBox.views.insert_cdma'),
    url(r'^insert_cdma1.do$', 'OutBox.views.insert1_cdma'),
)

