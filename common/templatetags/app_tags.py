# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()
 
@register.filter()
def currency(amount):
    dollars = round(float(amount), 2)
    return "£%s%s" % (intcomma(int(amount)), ("%0.2f" % amount)[-3:])
# https://stackoverflow.com/questions/346467/format-numbers-in-django-templates