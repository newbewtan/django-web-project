# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-11 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20180411_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='futures',
            field=models.CharField(default='', max_length=50, verbose_name='教学特点'),
        ),
    ]
