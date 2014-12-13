# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import RegexValidator


class SignUpForm(forms.Form):
    userid = forms.CharField(validators=[RegexValidator(regex=r'^[\d]{10}$', message=u'올바른 학번을 입력하세요')])
    email = forms.EmailField()
    password = forms.CharField()


class LoginForm(forms.Form):
    userid = forms.CharField()
    password = forms.CharField()


class AddStudentForm(forms.Form):
    student_id = forms.SlugField(validators=[RegexValidator(regex=r'^[\d]{10}$', message=u'올바른 학번을 입력하세요')])


class ValidateUseridForm(forms.Form):
    userid = forms.CharField()


class ValidateEmailForm(forms.Form):
    email = forms.EmailField()