# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20171008_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='expected_cal',
            field=models.IntegerField(default=0, help_text='Expected number of calories per day'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
