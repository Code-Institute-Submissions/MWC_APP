# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template

# https://stackoverflow.com/questions/1052531/get-user-group-in-a-template
#/templatetags have to be in an APP
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """ tag to check if current user belongs to user group """

    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.simple_tag
def css_colour(user):
    """ defines css colours for user groups users can belong to > 1 group but this 
        defines colours for window_cleaners and non-WC only. css colours as defined in materialize.css
    """

    groups = user.groups.all().values_list('name', flat=True)
    if 'window_cleaner' in groups:
        return 'blue'
    else:
        return 'teal'
