# -*- coding: utf-8 -*-
from django import forms

__author__ = 'sungjinyoo'


class TimeTableForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    grade = forms.IntegerField()
    week = forms.IntegerField()


class AttendanceForm(forms.Form):
    year = forms.IntegerField()
    semester = forms.IntegerField()
    grade = forms.IntegerField()
    course_no = forms.SlugField()
    block_data = forms.CharField()