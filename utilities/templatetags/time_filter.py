import datetime

from django import template
from django.db import models
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(name='convert_minutes_to_time')
def convert_minutes_to_time(value: int):
    hours = value // 60
    minutes = value % 60
    time = datetime.time(hour=hours, minute=minutes)
    return time.strftime('%H:%M')


@register.filter(name='duration_string_format')
def show_duration_in_string_format(value: int):
    if value is not None:
        hours = value // 60
        minutes = value % 60
        return str(hours) + ' ' + _('hours') + ' ' + _('and') + ' ' + str(minutes) + ' ' + _('minutes')
    return '00:00'
