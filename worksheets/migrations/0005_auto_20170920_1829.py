# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksheets', '0004_auto_20170918_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='job_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
