# -*- coding: utf-8 -*-
import json
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from core.views import LoginRequiredMixin
from teemo.forms import LoginForm, AddStudentForm
from time_table.models import add_student


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        # process login
        # redirect to main page on success

        form = LoginForm(request.POST)

        if not form.is_valid():
            return redirect(reverse('login'))

        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
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


class AddStudentView(LoginRequiredMixin, TemplateView):
    template_name = 'add_student.html'

    # generates an json response
    def post(self, request, *args, **kwargs):
        form = AddStudentForm(request.POST)

        if form.is_valid():
            result, toast_type, message = add_student(form.cleaned_data['student_id'])
        else:
            result = False
            toast_type = u'danger'
            message = u'올바른 학번을 입력해주세요'

        response_data = dict(
            result=result,
            toast_type=toast_type,
            message=message
        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')