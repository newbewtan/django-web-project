# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-04-09 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_auto_20180409_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='user_comment',
            field=models.CharField(default=[], max_length=50, verbose_name='用户评论'),
        ),
    ]
