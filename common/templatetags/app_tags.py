# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from worksheets.models import Job
from django.db.models import Sum


register = template.Library()


@register.filter()
def currency(amount):
    """ simple tag to return GBP currency - doesn't support localization """

    amount = round(float(amount), 2)
    return "£%s%s" % (intcomma(int(amount)), ("%0.2f" % amount)[-3:])
# https://stackoverflow.com/questions/346467/format-numbers-in-django-templates


@register.simple_tag()
def show_invoices(user):
    """ simple tag to return number of invoices, displayed as badges in menus """
    qs = Job.objects.filter(
        window_cleaner=user,
        job_status__job_status_description='Completed',
        invoiced=False).aggregate(Sum('price'))
    sum = qs['price__sum']
    if not sum:
        sum = 0.00
    return '£%s' % str(sum)


@register.simple_tag()
def show_owings(user):
    """ simple tag to return owings, displayed as badges in menus """
    qs = Job.objects.filter(
        window_cleaner=user,
        job_status__job_status_description='Completed',
        payment_status__payment_status_description='Owed').aggregate(
        Sum('price'))
    sum = qs['price__sum']
    if not sum:
        sum = 0.00
    return '£%s' % str(sum)
