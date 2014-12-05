# -*- coding: utf-8 -*-
import json
from django.core import serializers
from django.http.response import HttpResponse
from django.views.generic.base import View
from core.views import LoginRequiredMixin
from time_table.forms import TimeTableForm
from time_table.models import Course


class TimeTableView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # TODO: make grade option in place

        result = False
        data = []

        form = TimeTableForm(request.POST)
        if form.is_valid():
            form.cleaned_data['year']
            form.cleaned_data['semester']
            form.cleaned_data['grade']
            form.cleaned_data['week']

            # TODO: add filter for parameter week
            # start_date, end_date = get_dates_of_week()
            # TODO: add filter for grade
            data = json.loads(serializers.serialize(
                'json',
                Course.objects.filter(
                    year=form.cleaned_data['year'],
                    semester=form.cleaned_data['semester']
                ),
                relations=('course_times',)
            ))
            result = True
            type = u'success'
            message = u'시간표를 가져왔습니다'
        else:
            type = u'error'
            message = u'시간표를 가져오는데 실패하였습니다'

        response_data = dict(
            result=result,
            data=data,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class AttendanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        response_data = dict(

        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')
