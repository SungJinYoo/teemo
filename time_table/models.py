# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.decorators import method_decorator
from core.constants import WEEK_DAY_KEYS, TIME_TABLE_PERIODS, WEEK_DAY_TRANS_KOR_REVERSE
from core.utils import fetch_student_time_table, get_current_year, get_current_semester, fetch_courses
import re


class Univ(models.Model):
    organization_code = models.CharField(verbose_name=u'조직코드', max_length=30)
    univ_code = models.CharField(verbose_name=u'대학코드', max_length=30, primary_key=True)

    name = models.CharField(verbose_name=u'대학이름', max_length=60, null=True)

    def __unicode__(self):
        return u'{}({})'.format(self.name, self.univ_code)


class Department(models.Model):
    univ = models.ForeignKey(Univ, related_name='departments', null=True)

    department_code = models.CharField(verbose_name=u'학과코드', max_length=30, primary_key=True)

    name_ko = models.CharField(verbose_name=u'학과이름', max_length=150, null=True)
    name_en = models.CharField(verbose_name=u'학과이름(영문)', max_length=150, null=True)

    def __unicode__(self):
        return u'{}({})'.format(self.name_ko, self.department_code)


class CourseManager(models.Manager):
    @method_decorator(transaction.atomic)
    def create(self, year, semester, grade, name, name_en, course_no, time_infos):
        time_re = re.compile(
            r'[\d]{2}(:)?[\d]{2}'
        )

        try:
            course = Course.objects.filter(year=year, semester=semester, course_no=course_no).get()

        except Course.DoesNotExist:
            course = Course(year=year, semester=semester, grade=grade, course_no=course_no, name=name, name_en=name_en)
            course.save()

        course_times = course.course_times.all()

        import sys
        sys.stdout.write(course_no + " ")
        sys.stdout.write(name + " ")

        for time_info in time_infos:
            start_time = time_info['start_time']
            end_time = time_info['end_time']

            if not (time_re.match(start_time) and time_re.match(end_time)):
                raise ValidationError(u'시간의 형식에 맞지 않습니다')

            sys.stdout.write(time_info['start_time'] + " ")
            sys.stdout.write(time_info['end_time'] + " ///")
            if ":" in start_time:
                start_time = start_time[:2] + start_time[3:]
            if ":" in end_time:
                end_time = end_time[:2] + end_time[3:]

            sys.stdout.write(WEEK_DAY_TRANS_KOR_REVERSE[time_info['day']] + " ")
            sys.stdout.write(start_time + " ")
            sys.stdout.write(end_time + " ")
            for course_time in CourseTime.objects.filter(day=WEEK_DAY_TRANS_KOR_REVERSE[time_info['day']],
                                                         start_time__gte=start_time,
                                                         end_time__lte=end_time):
                if course_time not in course_times:
                    course.course_times.add(course_time)
        sys.stdout.write("\n")
        return course


class CourseTime(models.Model):
    WEEK_DAY_CHOICES = (
        (WEEK_DAY_KEYS[0], u'월요일'),
        (WEEK_DAY_KEYS[1], u'화요일'),
        (WEEK_DAY_KEYS[2], u'수요일'),
        (WEEK_DAY_KEYS[3], u'목요일'),
        (WEEK_DAY_KEYS[4], u'금요일'),
        (WEEK_DAY_KEYS[5], u'토요일'),
        (WEEK_DAY_KEYS[6], u'월요일')
    )

    day = models.CharField(verbose_name=u'요일', choices=WEEK_DAY_CHOICES, max_length=8, null=False, blank=False)
    period_index = models.IntegerField(verbose_name=u'교시', null=False, blank=False)
    start_time = models.CharField(verbose_name=u'시작시간', max_length=8, null=False, blank=False)
    end_time = models.CharField(verbose_name=u'종료시간', max_length=8, null=False, blank=False)

    def __unicode__(self):
        return u'{} {}~{}'.format(self.day, self.start_time, self.end_time)


class Course(models.Model):
    department = models.ForeignKey(Department, related_name='courses', null=True)
    course_times = models.ManyToManyField(CourseTime, related_name='courses')

    year = models.IntegerField(verbose_name=u'년도', null=False, blank=False)
    semester = models.IntegerField(verbose_name=u'학기', null=False, blank=False)
    grade = models.IntegerField(verbose_name=u'학년', null=False, blank=False)
    course_no = models.SlugField(verbose_name=u'학수번호', null=False, blank=False, unique=True)
    name = models.CharField(verbose_name=u'과목이름', max_length=128, null=False, blank=False)
    name_en = models.CharField(verbose_name=u'과목이름(영어)', max_length=128, null=False, blank=False)

    objects = CourseManager()

    def __unicode__(self):
        return u'{}-{}'.format(self.course_no, self.name)

    @staticmethod
    def update_courses(year, semester):
        course_info_list = fetch_courses(year, semester)
        for course_info in course_info_list:
            # year, semester, grade, name, course_no, time_infos
            time_info_list = list()
            if course_info['suupTimes']:
                for time in course_info['suupTimes'].split(','):
                    # 요일(start_time~end_time)
                    if len(time.split('(')) > 1:
                        day, rest = time.split('(')
                        start_time, end_time = rest[:-1].split('-')

                        time_info_list.append(dict(
                            day=day,
                            start_time=start_time,
                            end_time=end_time
                        ))

            course = Course.objects.create(year=year, semester=semester, grade=course_info['isuGrade'],
                                           name=course_info['gwamokNm'], name_en=course_info['gwamokEnm'],
                                           course_no=course_info['suupNo'], time_infos=time_info_list)


class ExtraManager(models.Manager):
    @method_decorator(transaction.atomic)
    def create(self, year, semester, course_no, week, category, memo, day, start_time, end_time, **kwargs):
        course = Course.objects.filter(year=year, semester=semester, course_no=course_no).get()

        extra = Extra(course=course, week=week, category=category, memo=memo)
        extra.save()

        course_times = CourseTime.objects.filter(day=day, start_time__gte=start_time, end_time__lte=end_time)
        for course_time in course_times:
            extra.course_times.add(course_time)

        return extra


class Extra(models.Model):
    ADDITIONAL = 0
    EXAM = 1

    EXTRA_CATEGORY_CHOICES = (
        (ADDITIONAL, u'보강'),
        (EXAM, u'시험'),
    )

    course = models.ForeignKey(Course, related_name='extras')
    course_times = models.ManyToManyField(CourseTime, related_name='extras')

    week = models.IntegerField(verbose_name=u'주차', null=False, blank=False)
    category = models.IntegerField(verbose_name=u'유형', null=False, blank=False, choices=EXTRA_CATEGORY_CHOICES)
    memo = models.CharField(verbose_name=u'메모', max_length=256, null=True, blank=True)

    objects = ExtraManager()

    def __unicode__(self):
        return u'{} {} {}'.format(self.week, self.type, self.course.name)


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    student_id = models.SlugField(verbose_name=u'학번', null=False, blank=False)
    courses = models.ManyToManyField(Course, related_name='students')

    def add_course(self):
        year = get_current_year()
        semester = get_current_semester()
        time_table_data = fetch_student_time_table(self.student_id, year, semester)

        for period_index, period_data in enumerate(time_table_data):
            for day in WEEK_DAY_KEYS:
                if period_data[day]:
                    course_no, name, trash1, trash2, trash3 = period_data[day].split(',')
                    course = Course.objects.filter(year=year, semester=semester, course_no=course_no).get()
                    self.courses.add(course)

    def __unicode__(self):
        return u'{}'.format(self.student_id)


def add_student(student_id):
    student, is_new = Student.objects.get_or_create(student_id=student_id)

    try:
        student.add_course()
        return True, u'success', u'학번 {} 추가되었습니다'.format(student.student_id)
    except Exception as e:
        return False, u'danger', u'학생 추가에 실패하였습니다'

