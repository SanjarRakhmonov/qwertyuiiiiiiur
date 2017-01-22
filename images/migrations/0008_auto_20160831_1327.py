# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 13:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('images', '0007_auto_20160829_1812'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ('-created',), 'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.RenameField(
            model_name='image',
            old_name='description',
            new_name='caption',
        ),
        migrations.AddField(
            model_name='image',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_parent', to='images.Image'),
        ),
        migrations.AddField(
            model_name='image',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='image',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images_created', to=settings.AUTH_USER_MODEL),
        ),
    ]
