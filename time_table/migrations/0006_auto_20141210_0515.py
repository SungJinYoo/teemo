# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_table', '0005_auto_20141209_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='memo',
            field=models.CharField(max_length=256, null=True, verbose_name='\uba54\ubaa8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='univ',
            name='name',
            field=models.CharField(max_length=60, null=True, verbose_name='\ub300\ud559\uc774\ub984'),
            preserve_default=True,
        ),
    ]
