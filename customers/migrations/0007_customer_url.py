# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-24 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_customer_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
