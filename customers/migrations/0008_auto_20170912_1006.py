# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_auto_20170912_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='property_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='customers.Property_type'),
        ),
    ]
