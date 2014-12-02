# -*- coding: utf-8 -*-
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from teemo.forms import LoginForm


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