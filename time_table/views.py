# -*- coding: utf-8 -*-
import json
from django.core import serializers
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from core.constants import WEEK_DAY_TRANS_KOR, SEMESTER_TRANS
from core.views import LoginRequiredForAjaxMixin
from time_table.forms import TimeTableForm, AttendanceForm, ExtraForm, FetchExtraForm, StudentTimeTableForm
from time_table.models import Course, CourseTime, Extra, User


class TimeTableView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        # TODO: make grade option in place

        result = False
        data = []
        type = u'error'
        message = u'시간표를 가져오는데 실패하였습니다'

        form = TimeTableForm(request.POST)
        if form.is_valid():
            try:
                course = Course.objects.filter(year=form.cleaned_data['year'],
                                               semester=form.cleaned_data['semester'],
                                               course_no=form.cleaned_data['course_no']).get()
                data = json.loads(serializers.serialize(
                    'json',
                    Course.objects.filter(students__in=User.objects.filter(courses=course)),
                    relations=('course_times',)
                ))
                result = True
                type = u'success'
                message = u'''<strong>{}-{}</strong>을(를) 듣는 학생들의 <strong>{}주차</strong> 종합 시간표를 가져왔습니다''' \
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


class StudentTimeTableView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        form = StudentTimeTableForm(request.POST)

        result = False
        data = dict()

        if form.is_valid():
            data = json.loads(serializers.serialize(
                'json',
                request.user.courses.filter(year=form.cleaned_data['year'],
                                            semester=form.cleaned_data['semester']),
                relations=('course_times',)
            ))

            result = True

        response_data = dict(
            result=result,
            data=data,
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class AttendanceView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        form = AttendanceForm(request.POST)

        result = False
        data = {}
        type=u'error'
        message = u'출석 예상 정보를 불러오는데 실패하였습니다'

        if form.is_valid():
            block_data = json.loads(form.cleaned_data['block_data'])

            course = Course.objects.filter(year=form.cleaned_data['year'], semester=form.cleaned_data['semester'], course_no=form.cleaned_data['course_no']).get()
            students = User.objects.filter(courses=course)  # all the students that attends this course
            course_times = CourseTime.objects.filter(day=block_data['day'], period_index__in=block_data['period_index_list'])
            students_that_expected_to_dismiss = students.filter(courses__in=Course.objects.filter(course_times__in=course_times))

            total_students = students.count()
            dismiss_students = students_that_expected_to_dismiss.count()

            result = True
            data = dict(form.cleaned_data)
            data['total_students'] = total_students
            data['dismiss_students'] = dismiss_students
            del data['block_data']
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


class ExtraView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        form = ExtraForm(request.POST)

        result = False
        data = {}
        type=u'error'
        message = u'일정 추가에 실패하였습니다'

        if form.is_valid():
            extra = Extra.objects.create(**form.cleaned_data)
            if extra:
                result = True
                data = dict(
                    extra_data=json.loads(serializers.serialize(
                        'json',
                        [extra],
                        relations=('course_times', 'course')
                    )),
                    attendance_info_no=form.cleaned_data['attendance_info_no']
                )
                data['attendance_info_no'] = form.cleaned_data['attendance_info_no']
                type = u'success'
                message = u'일정이 추가되었습니다'

        response_data = dict(
            result=result,
            data=data,
            type=type,
            message=message
        )
        return HttpResponse(json.dumps(response_data), content_type='application/json')


class ModifyExtraView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        result = False,
        type = u'error',
        message = u'교수의 권한이 필요합니다'

        if request.user.is_professor():
            extra = Extra.objects.get(pk=request.POST['extra_pk'])

            if extra.course in request.user.teaching_courses.all():
                extra.category = request.POST['category']
                extra.memo = request.POST['memo']
                extra.save()

                result = True
                type = u'success'
                message = u'일정이 수정되었습니다'

            else:
                message = u'담당 교과목이 아닙니다'

        response_data = dict(
            result=result,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class DeleteExtraView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        result = False,
        type = u'error',
        message = u'교수의 권한이 필요합니다'

        if request.user.is_professor():
            extra = Extra.objects.get(pk=request.POST['extra_pk'])

            if extra.course in request.user.teaching_courses.all():
                extra.delete()

                result = True
                type = u'success'
                message = u'일정이 취소되었습니다'

            else:
                message = u'담당 교과목이 아닙니다'
                
        response_data = dict(
            result=result,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class ExtraListView(LoginRequiredForAjaxMixin, View):
    def post(self, request, *args, **kwargs):
        form = FetchExtraForm(request.POST)

        result = False
        data = {}
        type=u'error'
        message = u'일정 조회에 실패하였습니다'

        if form.is_valid():
            course = Course.objects.filter(year=form.cleaned_data['year'],
                                           semester=form.cleaned_data['semester'],
                                           course_no=form.cleaned_data['course_no'])
            extras = Extra.objects.filter(course=course, week=form.cleaned_data['week'])

            result = True
            data = json.loads(serializers.serialize(
                'json',
                extras,
                relations=('course_times', 'course')
            ))
            type = u'success'
            message = u'{}년 {}학기 {}주차 일정을 조회하였습니다'.format(form.cleaned_data['year'],
                                                          SEMESTER_TRANS[form.cleaned_data['semester']],
                                                          form.cleaned_data['week'])

        response_data = dict(
            result=result,
            data=data,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')