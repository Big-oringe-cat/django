from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^flowreceive', 'LiuliangQuery.views.flowreceive'),
)

