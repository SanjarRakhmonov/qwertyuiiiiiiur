# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-19 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_image_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='total_likes',
        ),
        migrations.RemoveField(
            model_name='image',
            name='users_like',
        ),
        migrations.AddField(
            model_name='image',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='image',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
