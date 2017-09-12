# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksheets', '0008_auto_20170912_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='customers.Customer'),
        ),
    ]
