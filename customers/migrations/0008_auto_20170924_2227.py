# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_customer_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='latitude',
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='longitude',
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
