from django import template

register = template.Library()

@register.filter
def running_total(date_list):
    return sum(d.price for d in date_list)

@register.filter
def mul(value, arg):
    return value*arg