# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_table', '0002_auto_20141204_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetime',
            name='day',
            field=models.CharField(default='yoil2', max_length=8, verbose_name='\uc694\uc77c'),
            preserve_default=False,
        ),
    ]
