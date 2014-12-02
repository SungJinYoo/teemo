# -*- coding: utf-8 -*-

from django.db import models


class Course(models.Model):
    pass


class Student(models.Model):
    student_id = models.IntegerField(verbose_name=u'학번', null=False, blank=False)
    courses = models.ManyToManyField(Course, related_name='students')

# Create your models here.
