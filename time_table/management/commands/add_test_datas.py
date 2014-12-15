# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from time_table.models import add_student, User, Course

__author__ = 'sungjinyoo'

class Command(BaseCommand):
    help = u'make test data'
    
    def handle(self, *args, **options):
        u = User.objects.create_professor(u'teemo', u'teemo')
        c = Course.objects.get(course_no=22152)
        c.professor = u
        c.save()
        
        add_student(u"2008037280")
        add_student(u"2012036815")
        add_student(u"2012037158")

        signupdata = dict(
            userid=u"2008037280",
            email=u"dosm123@asdfasdf.com",
            password=u"2008037280"
        )

        User.objects.get_or_create_student(**signupdata)
