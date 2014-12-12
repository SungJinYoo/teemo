# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from time_table.views import *

urlpatterns = patterns('',
                       url(r'^$', TimeTableView.as_view(), name='fetch'),
                       url(r'^attendance/$', AttendanceView.as_view(), name='attendance'),
                       url(r'^extra/$', ExtraView.as_view(), name='extra'),
                       url(r'^extras/$', ExtraListView.as_view(), name='extras'),
                       url(r'^modify_extra/$', ModifyExtraView.as_view(), name='modify_extra'),
                       url(r'^delete_extra/$', DeleteExtraView.as_view(), name='delete_extra')
)
