# -*- coding: utf-8 -*-
import json
from django.core import serializers
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.generic.base import View
from core.constants import WEEK_DAY_TRANS_KOR
from core.views import LoginRequiredMixin
from time_table.forms import TimeTableForm, AttendanceForm
from time_table.models import Course, Student, CourseTime


class TimeTableView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # TODO: make grade option in place

        result = False
        data = []
        type = u'error'
        message = u'시간표를 가져오는데 실패하였습니다'

        form = TimeTableForm(request.POST)
        if form.is_valid():
            try:
                course = Course.objects.filter(course_no=form.cleaned_data['course_no']).get()
                data = json.loads(serializers.serialize(
                    'json',
                    Course.objects.filter(students__in=Student.objects.filter(courses=course)),
                    relations=('course_times',)
                ))
                result = True
                type = u'success'
                message = u'''<strong>{}-{}</strong>을(를) 듣는 학생들의 <strong>{}주차</strong> 종합 시간표를 가져왔습니다'''\
                    .format(course.course_no, course.name, form.cleaned_data['week'])
            except:
                pass

        response_data = dict(
            result=result,
            data=data,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class AttendanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)

        result = False
        data = {}
        type=u'error'
        message = u'출석 예상 정보를 불러오는데 실패하였습니다'

        if form.is_valid():
            block_data = json.loads(form.cleaned_data['block_data'])

            course = Course.objects.filter(course_no=form.cleaned_data['course_no']).get()
            students = Student.objects.filter(courses=course)  # all the students that attends this course
            course_times = CourseTime.objects.filter(day=block_data['day'], period_index__in=block_data['period_index_list'])
            students_that_expected_to_dismiss = students.filter(courses__in=Course.objects.filter(course_times__in=course_times))

            total_students = students.count()
            dismiss_students = students_that_expected_to_dismiss.count()

            result = True
            data = dict(
                block_no=form.cleaned_data['block_no'],
                total_students=total_students,
                dismiss_students=dismiss_students,
            )
            type = u'success'
            message = u'출석 예상 정보를 가져왔습니다<br/>({} {}~{}교시)'.format(WEEK_DAY_TRANS_KOR[block_data['day']],
                                                             int(block_data['period_index_list'][0]) + 1,
                                                             int(block_data['period_index_list'][len(block_data['period_index_list']) - 1]) + 1)


        response_data = dict(
            result=result,
            data=data,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')
