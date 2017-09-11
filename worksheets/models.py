# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

class Job_status(models.Model):
    job_status = models.IntegerField()
    job_status_description = models.CharField(max_length=50, blank=False, null=False)

class Payment_status(models.Model):
    payment_status = models.IntegerField()
    payment_status_description = models.CharField(max_length=50, blank=False, null=False)

class Jobs(models.Model):
    FREQUENCY_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (4, 4),
        (8, 8),
        (12, 12),
        (16, 16),
        (20, 20),
        (24, 24),
        (26, 26),
        (52, 52)
    )
    customer = models.ForeignKey('customers.Customer', null=False, related_name='jobs')
    scheduled_date = models.DateField(null=False)
    allocated_date = models.DateField(null=True)
    completed_date = models.DateField(null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    job_notes = models.TextField(blank=True, null=True)
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES, null=False)
    job_status = models.ForeignKey(Job_status, null=False)
    payment_status = models.ForeignKey(Payment_status, null=True)
    job_notes = models.TextField(blank=True)
    window_cleaner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=None, null=True, related_name='jobs')
    