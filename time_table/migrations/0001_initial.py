# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(verbose_name='\ub144\ub3c4')),
                ('semester', models.IntegerField(verbose_name='\ud559\uae30')),
                ('grade', models.IntegerField(verbose_name='\ud559\ub144')),
                ('course_no', models.SlugField(unique=True, verbose_name='\ud559\uc218\ubc88\ud638')),
                ('name', models.CharField(max_length=128, verbose_name='\uacfc\ubaa9\uc774\ub984')),
                ('start_time', models.CharField(max_length=8, verbose_name='\uc2dc\uc791\uc2dc\uac04')),
                ('end_time', models.CharField(max_length=8, verbose_name='\uc885\ub8cc\uc2dc\uac04')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period_index', models.IntegerField(verbose_name='\uad50\uc2dc')),
                ('start_time', models.SmallIntegerField(verbose_name='\uc2dc\uc791\uc2dc\uac04')),
                ('end_time', models.SmallIntegerField(verbose_name='\uc885\ub8cc\uc2dc\uac04')),
                ('course', models.ManyToManyField(related_name='course_times', to='time_table.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_id', models.SlugField(verbose_name='\ud559\ubc88')),
                ('courses', models.ManyToManyField(related_name='students', to='time_table.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
