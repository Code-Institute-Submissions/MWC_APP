# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models import Sum


class JobStatus(models.Model):
    job_status_description = models.CharField(
        max_length=50, blank=False, null=False)

    def __str__(self):
        return self.job_status_description

    verbose_name_plural = "job_statuses"


class PaymentStatus(models.Model):
    payment_status_description = models.CharField(
        max_length=50, blank=False, null=False)

    def __str__(self):
        return self.payment_status_description

    verbose_name_plural = "payment_statuses"


class Job(models.Model):
    customer = models.ForeignKey(
        'customers.Customer',
        null=False,
        related_name='jobs')
    scheduled_date = models.DateField(null=False)
    allocated_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    job_notes = models.TextField(blank=True, null=True)
    job_status = models.ForeignKey(JobStatus, null=False)
    payment_status = models.ForeignKey(PaymentStatus, blank=True, null=True)
    job_notes = models.TextField(blank=True, null=True)
    window_cleaner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=None,
        blank=True,
        null=True,
        related_name='jobs',
        limit_choices_to={
            'groups__name': 'window_cleaner'})
    invoiced = models.NullBooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return str(self.scheduled_date)

    @property
    def total(self):
        qs = Jobs.objects.filter(id=self).aggregate(Sum('price'))
        sum = qs['price__sum']
        if not sum:
            sum = 0.00
        return sum
