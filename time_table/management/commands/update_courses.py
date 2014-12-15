# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from time_table.models import Course

__author__ = 'sungjinyoo'


class Command(BaseCommand):
    help = u'update course info from ezhub'

    def handle(self, *args, **options):
        Course.update_courses(*args)

