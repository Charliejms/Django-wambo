from urllib.parse import quote_plus
from django import template

#filtros personalizados  en los Templates
register = template.Library()


@register.filter
def urlify_twitter(value):
    return quote_plus(value)