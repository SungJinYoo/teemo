# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('time_table', '0003_coursetime_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.IntegerField(verbose_name='\uc8fc\ucc28')),
                ('type', models.IntegerField(verbose_name='\ud0c0\uc785', choices=[(1, '\ubcf4\uac15'), (2, '\uc2dc\ud5d8')])),
                ('course', models.ForeignKey(related_name='extras', to='time_table.Course')),
                ('course_times', models.ManyToManyField(related_name='extra', to='time_table.CourseTime')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
