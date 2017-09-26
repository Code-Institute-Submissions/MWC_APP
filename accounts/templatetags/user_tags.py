# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template

# https://stackoverflow.com/questions/1052531/get-user-group-in-a-template
#/templatetags have to be in an APP
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False
