from django import template

register = template.Library()


@register.filter
def running_total(date_list):
    """ used to sum regroup over dates groups """
    return sum(d.price for d in date_list)


@register.filter
def multiply(value, arg):
    """ used to multiply values in templates (for Stripe) """
    return value * arg
