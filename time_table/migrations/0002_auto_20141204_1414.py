# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_table', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='course',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='coursetime',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='course_times',
            field=models.ManyToManyField(related_name='courses', to='time_table.CourseTime'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='end_time',
            field=models.CharField(max_length=8, verbose_name='\uc885\ub8cc\uc2dc\uac04'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='start_time',
            field=models.CharField(max_length=8, verbose_name='\uc2dc\uc791\uc2dc\uac04'),
            preserve_default=True,
        ),
    ]
