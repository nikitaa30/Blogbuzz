# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-29 23:26
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=blog.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('body', models.TextField()),
                ('date', models.DateTimeField()),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
