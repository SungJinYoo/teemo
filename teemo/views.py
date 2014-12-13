# -*- coding: utf-8 -*-
import json
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from core.views import LoginRequiredForAjaxMixin
from teemo.forms import LoginForm, AddStudentForm, SignUpForm, ValidateUseridForm, ValidateEmailForm
from time_table.models import add_student, User


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            User.objects.get_or_create_student(**form.cleaned_data)

            user = authenticate(username=form.cleaned_data['userid'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                print 'user cannot be created'
        else:
            print 'invalid form data'

        return redirect(reverse('index'))


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        # process login
        # redirect to main page on success

        form = LoginForm(request.POST)

        if not form.is_valid():
            return redirect(reverse('login'))

        user = authenticate(username=form.cleaned_data['userid'], password=form.cleaned_data['password'])
        if not user:
            # invalid username or password
            return redirect(reverse('login'))

        if not user.is_active:
            # user is not active(removed)
            print 'user is not active'
            return redirect(reverse('login'))

        login(request, user)

        return redirect(reverse('index'))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('index'))


class AddStudentView(LoginRequiredForAjaxMixin, TemplateView):
    template_name = 'add_student.html'

    # generates an json response
    def post(self, request, *args, **kwargs):
        form = AddStudentForm(request.POST)

        result = False
        type = u'danger'
        message = u'올바른 학번을 입력해주세요'

        if form.is_valid():
            result, type, message = add_student(form.cleaned_data['student_id'])

        response_data = dict(
            result=result,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class ValidateUseridView(View):
    def post(self, request, *args, **kwargs):
        form = ValidateUseridForm(request.POST)

        result = False
        type = u'error'
        message = u'사용 불가능한 <strong>학번</strong>입니다'

        if form.is_valid():
            try:
                user = User.objects.filter(userid=form.cleaned_data['userid'], is_active=True).get()
            except:
                # no user. you can use it
                result = True
                type = u'success'
                message = u'사용 가능한 <strong>학번</strong>입니다'

        response_data = dict(
            result=result,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class ValidateEmailView(View):
    def post(self, request, *args, **kwargs):
        form = ValidateEmailForm(request.POST)

        result = False
        type = u'error'
        message = u'사용 불가능한 <strong>이메일</strong>입니다'

        if form.is_valid():
            try:
                user = User.objects.filter(userid=form.cleaned_data['email'], is_active=True).get()
            except:
                # no user. you can use it
                result = True
                type = u'success'
                message = u'사용 가능한 <strong>이메일</strong>입니다'

        response_data = dict(
            result=result,
            type=type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')