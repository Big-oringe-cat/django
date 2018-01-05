from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^chart','Chart.views.chart'),
    url(r'^alarm_statistics','Chart.views.alarm_statistics'),
    url(r'^select','Chart.views.select'),
    url(r'^alarm_detail','Chart.views.alarm_detail'),
)
