# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.decorators import method_decorator
from core.constants import WEEK_DAY_KEYS, TIME_TABLE_PERIODS
from core.utils import fetch_student_time_table, get_current_year, get_current_semester
import re


class CourseManager(models.Manager):
    @method_decorator(transaction.atomic)
    def create(self, year, semester, grade, name, course_no, day, start_time, end_time):
        time_re = re.compile(
            r'[\d]{2}(:)?[\d]{2}'
        )
        if not(time_re.match(start_time) and time_re.match(end_time)):
            raise ValidationError(u'시간의 형식에 맞지 않습니다')

        if ":" in start_time:
            start_time = start_time[:2] + start_time[2:]
        if ":" in end_time:
            end_time = end_time[:2] + end_time[2:]

        try:
            course = Course.objects.filter(year=year, semester=semester, course_no=course_no).get()
            course_times = course.course_times.all()
            for course_time in CourseTime.objects.filter(day=day, start_time__gte=start_time, end_time__lte=end_time):
                if course_time not in course_times:
                    course.course_times.add(course_time)
        except Course.DoesNotExist:
            course = Course(year=year, semester=semester, grade=grade, course_no=course_no, name=name)
            course.save()
            for course_time in CourseTime.objects.filter(day=day, start_time__gte=start_time, end_time__lte=end_time):
                course.course_times.add(course_time)

        return course


class CourseTime(models.Model):
    day = models.CharField(verbose_name=u'요일', max_length=8, null=False, blank=False)
    period_index = models.IntegerField(verbose_name=u'교시', null=False, blank=False)
    start_time = models.CharField(verbose_name=u'시작시간', max_length=8, null=False, blank=False)
    end_time = models.CharField(verbose_name=u'종료시간', max_length=8, null=False, blank=False)


class Course(models.Model):
    course_times = models.ManyToManyField(CourseTime, related_name='courses')

    year = models.IntegerField(verbose_name=u'년도', null=False, blank=False)
    semester = models.IntegerField(verbose_name=u'학기', null=False, blank=False)
    grade = models.IntegerField(verbose_name=u'학년', null=False, blank=False)
    course_no = models.SlugField(verbose_name=u'학수번호', null=False, blank=False, unique=True)
    name = models.CharField(verbose_name=u'과목이름', max_length=128, null=False, blank=False)

    objects = CourseManager()


class Student(models.Model):
    student_id = models.SlugField(verbose_name=u'학번', null=False, blank=False)
    courses = models.ManyToManyField(Course, related_name='students')

    def add_course(self):
        year = get_current_year()
        semester = get_current_semester()
        time_table_data = fetch_student_time_table(self.student_id, year, semester)

        week_course_dict = {day: None for day in WEEK_DAY_KEYS}

        for period_index, period_data in enumerate(time_table_data):
            start_time, end_time = TIME_TABLE_PERIODS[period_index]
            for day in WEEK_DAY_KEYS:
                if period_data[day]:
                    course_no, name, trash1, trash2, trash3 = period_data[day].split(',')
                    if week_course_dict[day]:
                        week_course_dict[day]['end_time'] = end_time
                    else:
                        week_course_dict[day] = dict(
                            year=year,
                            semester=semester,
                            grade=0,
                            course_no=course_no,
                            name=name,
                            start_time=start_time,
                            day=day,
                        )
                else:
                    if week_course_dict[day]:
                        course = Course.objects.create(**week_course_dict[day])
                        self.courses.add(course)
                        week_course_dict[day] = None


def add_student(student_id):
    student, is_new = Student.objects.get_or_create(student_id=student_id)

    try:
        student.add_course()
        return True, u'success', u'학번 {} 추가되었습니다'.format(student.student_id)
    except Exception as e:
        return False, u'danger', u'학생 추가에 실패하였습니다'
