# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-19 00:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_image_users_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 19, 0, 59, 26, 691082)),
            preserve_default=False,
        ),
    ]
