# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_table', '0004_auto_20141208_0719'),
    ]

    operations = [
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
            name='Univ',
            fields=[
                ('organization_code', models.CharField(max_length=30, verbose_name='\uc870\uc9c1\ucf54\ub4dc')),
                ('univ_code', models.CharField(max_length=30, serialize=False, verbose_name='\ub300\ud559\ucf54\ub4dc', primary_key=True)),
                ('name', models.CharField(max_length=60, null=True, verbose_name='\ub300\ud559\ucf54\ub4dc')),
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
            name='department',
            field=models.ForeignKey(related_name='courses', to='time_table.Department', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='name_en',
            field=models.CharField(default='', max_length=128, verbose_name='\uacfc\ubaa9\uc774\ub984(\uc601\uc5b4)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursetime',
            name='day',
            field=models.CharField(max_length=8, verbose_name='\uc694\uc77c', choices=[('yoil2', '\uc6d4\uc694\uc77c'), ('yoil3', '\ud654\uc694\uc77c'), ('yoil4', '\uc218\uc694\uc77c'), ('yoil5', '\ubaa9\uc694\uc77c'), ('yoil6', '\uae08\uc694\uc77c'), ('yoil7', '\ud1a0\uc694\uc77c'), ('yoil0', '\uc6d4\uc694\uc77c')]),
            preserve_default=True,
        ),
    ]
