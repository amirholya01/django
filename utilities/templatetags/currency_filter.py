from django import template

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    if value is not None and value != 0:
        return '{:,}'.format(value)
    else:
        return 0
