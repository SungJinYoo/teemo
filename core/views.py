# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.views.generic.base import View


class LoginRequiredMixin(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class LoginRequiredForAjaxMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied()
        return super(LoginRequiredForAjaxMixin, self).dispatch(request, *args, **kwargs)

