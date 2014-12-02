# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from time_table.views import *

urlpatterns = patterns('',
                       url(r'^$', TimeTableView.as_view(), name='fetch'),
                       url(r'^attendance/$', AttendanceView.as_view(), name='attendance'),
)
