# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
from worksheets.models import Job

register = template.Library()


@register.simple_tag
def due_job_exists(customerid):
    """ to check if a ddue job exists for a customer """

    return Job.objects.filter(
        customer=customerid,
        completed_date__isnull=True).exists()


@register.simple_tag
def job_is_owed(job_status):
    """ to check if job.payment_status is 'owed'. Used in if block to change css in job list """

    if str(job_status) == 'Owed':
        return True
    else:
        return False
    # TODO: why do I need str()?


@register.simple_tag
def job_is_booked(payment_status):
    """ to check if job.payment_status is 'owed'. Used in if block to change css in job list """

    if str(payment_status) == 'Booked':
        return True
    else:
        return False
    # TODO: why do I need str()?
