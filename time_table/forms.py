# -*- coding: utf-8 -*-
from django import forms

__author__ = 'sungjinyoo'


class TimeTableForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    course_no = forms.SlugField()
    week = forms.IntegerField()


class AttendanceForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    week = forms.IntegerField()
    course_no = forms.SlugField()
    block_no = forms.IntegerField()
    block_data = forms.CharField()


class ExtraForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    course_no = forms.SlugField()
    week = forms.IntegerField()
    category = forms.IntegerField()
    memo = forms.CharField(required=False)
    day = forms.CharField()
    start_time = forms.CharField()
    end_time = forms.CharField()
    attendance_info_no = forms.IntegerField()


class FetchExtraForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    course_no = forms.SlugField()
    week = forms.IntegerField()
