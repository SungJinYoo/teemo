# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('userid', models.CharField(help_text='\uc544\uc774\ub514 \ud639\uc740 \ud559\ubc88', unique=True, max_length=60, verbose_name='\uc544\uc774\ub514', db_index=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name='\uc774\ub984', blank=True)),
                ('email', models.EmailField(max_length=255, unique=True, null=True, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, help_text=b'Is this user a staff?', verbose_name=b'is staff')),
                ('is_active', models.BooleanField(default=True, help_text=b'Is this user active?', verbose_name=b'is active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name': '\uc0ac\uc6a9\uc790',
                'verbose_name_plural': '\uc0ac\uc6a9\uc790\ub4e4',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(verbose_name='\ub144\ub3c4')),
                ('semester', models.IntegerField(verbose_name='\ud559\uae30')),
                ('grade', models.IntegerField(verbose_name='\ud559\ub144')),
                ('course_no', models.SlugField(unique=True, verbose_name='\ud559\uc218\ubc88\ud638')),
                ('name', models.CharField(max_length=128, verbose_name='\uacfc\ubaa9\uc774\ub984')),
                ('name_en', models.CharField(max_length=128, verbose_name='\uacfc\ubaa9\uc774\ub984(\uc601\uc5b4)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=8, verbose_name='\uc694\uc77c', choices=[('yoil2', '\uc6d4\uc694\uc77c'), ('yoil3', '\ud654\uc694\uc77c'), ('yoil4', '\uc218\uc694\uc77c'), ('yoil5', '\ubaa9\uc694\uc77c'), ('yoil6', '\uae08\uc694\uc77c'), ('yoil7', '\ud1a0\uc694\uc77c'), ('yoil0', '\uc6d4\uc694\uc77c')])),
                ('period_index', models.IntegerField(verbose_name='\uad50\uc2dc')),
                ('start_time', models.CharField(max_length=8, verbose_name='\uc2dc\uc791\uc2dc\uac04')),
                ('end_time', models.CharField(max_length=8, verbose_name='\uc885\ub8cc\uc2dc\uac04')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_code', models.CharField(max_length=30, serialize=False, verbose_name='\ud559\uacfc\ucf54\ub4dc', primary_key=True)),
                ('name_ko', models.CharField(max_length=150, null=True, verbose_name='\ud559\uacfc\uc774\ub984')),
                ('name_en', models.CharField(max_length=150, null=True, verbose_name='\ud559\uacfc\uc774\ub984(\uc601\ubb38)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField(verbose_name='\uc8fc\ucc28')),
                ('category', models.IntegerField(verbose_name='\uc720\ud615', choices=[(0, '\ubcf4\uac15'), (1, '\uc2dc\ud5d8')])),
                ('memo', models.CharField(max_length=256, null=True, verbose_name='\uba54\ubaa8', blank=True)),
                ('course', models.ForeignKey(related_name='extras', to='time_table.Course')),
                ('course_times', models.ManyToManyField(related_name='extras', to='time_table.CourseTime')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Univ',
            fields=[
                ('organization_code', models.CharField(max_length=30, verbose_name='\uc870\uc9c1\ucf54\ub4dc')),
                ('univ_code', models.CharField(max_length=30, serialize=False, verbose_name='\ub300\ud559\ucf54\ub4dc', primary_key=True)),
                ('name', models.CharField(max_length=60, null=True, verbose_name='\ub300\ud559\uc774\ub984')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='department',
            name='univ',
            field=models.ForeignKey(related_name='departments', to='time_table.Univ', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='course_times',
            field=models.ManyToManyField(related_name='courses', to='time_table.CourseTime'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(related_name='courses', to='time_table.Department', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='professor',
            field=models.ForeignKey(related_name='teaching_courses', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
