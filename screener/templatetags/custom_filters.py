from django import template

register = template.Library()


@register.filter
def concatenate(str1, str2):
    return str1 + str2
