# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-07 10:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180401_1547'),
        ('courses', '0007_course_class_nums'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teachers', verbose_name='授课讲师'),
        ),
    ]
