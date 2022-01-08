
from django import template


register = template.Library()


@register.filter(name='show')
def show(value):
    if str(value).split('.')[-1] in ['jpeg', 'jpg', 'png']:
        return value
    return None
