import random

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def replace_static(value):
    static_symbols = ["🎙", "💾", "🎛", "📟", "📽", "📺"]
    return value.replace("[static]", random.choice(static_symbols))
