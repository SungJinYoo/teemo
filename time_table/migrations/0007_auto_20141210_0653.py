# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_table', '0006_auto_20141210_0515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extra',
            name='type',
        ),
        migrations.AddField(
            model_name='extra',
            name='category',
            field=models.IntegerField(default=0, verbose_name='\uc720\ud615', choices=[(1, '\ubcf4\uac15'), (2, '\uc2dc\ud5d8')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='extra',
            name='course_times',
            field=models.ManyToManyField(related_name='extras', to='time_table.CourseTime'),
            preserve_default=True,
        ),
    ]
