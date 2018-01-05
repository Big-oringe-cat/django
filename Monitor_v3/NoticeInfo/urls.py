from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^select', 'NoticeInfo.views.select'),
    url(r'^Myalarm', 'NoticeInfo.views.Myalarm'),
    url(r'^Myignore', 'NoticeInfo.views.Myignore'),
    url(r'^addReason', 'NoticeInfo.views.addReason'),
    url(r'^Oper_recover', 'NoticeInfo.views.ignore'),
    url(r'^ignore', 'NoticeInfo.views.ignore'),
    url(r'^reason_select', 'NoticeInfo.views.reason_select'),
    url(r'^newreason_select', 'NoticeInfo.views.newreason_select'),
    url(r'^recovered_select', 'NoticeInfo.views.recovered_select'),
    url(r'^NIselect_Ignored_select', 'NoticeInfo.views.NIselect_Ignored_select'),
    url(r'^notice_detail', 'NoticeInfo.views.notice_detail'),
    url(r'^recover$', 'NoticeInfo.views.recover'),
    url(r'^recover_add_reason$', 'NoticeInfo.views.recover_add_reason'),
    url(r'^recover_add_reason2', 'NoticeInfo.views.recover_add_reason2'),
    url(r'^recover_reason$', 'NoticeInfo.views.recover_reason'),
    url(r'^recover_reason2', 'NoticeInfo.views.recover_reason2'),
    url(r'^FailureNotification', 'NoticeInfo.views.FailureNotification'),
    url(r'^alarm_detail', 'NoticeInfo.views.alarm_detail'),
)

