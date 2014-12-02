# -*- coding: utf-8 -*-
import json
from django.http.response import HttpResponse
from django.views.generic.base import View
from core.views import LoginRequiredMixin


class TimeTableView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # in request.POST week number
        response_data = dict(

        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')


class AttendanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        response_data = dict(

        )

        return HttpResponse(json.dumps(response_data), content_type='application/json')
