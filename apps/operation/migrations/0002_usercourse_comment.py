# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-09 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='comment',
            field=models.TextField(default=0, max_length=50, verbose_name='用户课程评论'),
        ),
    ]