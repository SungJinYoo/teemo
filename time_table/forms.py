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