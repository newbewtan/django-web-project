# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-09 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_course_res'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_res',
            field=models.FileField(upload_to='courses/course_res/%Y%m', verbose_name='课程资源'),
        ),
    ]