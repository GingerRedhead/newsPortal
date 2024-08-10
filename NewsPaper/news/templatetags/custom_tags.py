from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag()
def use_time(value, format_string='%b %d %Y'):
   return value.strftime(format_string)