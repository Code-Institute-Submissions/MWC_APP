# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
import locale
locale.setlocale(locale.LC_ALL, '')

register = template.Library()
 
@register.filter()
def currency(value):
    return 'ok' #locale.currency(value, grouping=True)