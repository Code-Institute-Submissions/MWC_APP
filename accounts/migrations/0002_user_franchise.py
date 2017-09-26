# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 19:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('franchises', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='franchise',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, to='franchises.Franchise'),
            preserve_default=False,
        ),
    ]
