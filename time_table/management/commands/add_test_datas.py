# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from time_table.models import add_student, User, Course

__author__ = 'sungjinyoo'

class Command(BaseCommand):
    help = u'make test data'
    
    def handle(self, *args, **options):
        u = User.objects.create_professor('teemo', 'teemo')
        c = Course.objects.get(course_no=22152)
        c.professor = u
        c.save()
        
        add_student("2008037280")
        add_student("2012036815")
        add_student("2012037158")

        signupdata = dict(
            userid="2008037280",
            email="dosm123@asdfasdf.com",
            password="2008037280"
        )

        User.objects.get_or_create_student(**signupdata)
