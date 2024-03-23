from django import template
from django.template.defaultfilters import stringfilter
from django.utils.text import Truncator

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def truncatewords_without_dots(value, arg):
    """
    Truncate a string after `arg` number of words.
    Remove newlines within the string.
    """
    try:
        length = int(arg)
    except ValueError:  # Invalid literal for int().
        return value  # Fail silently.
    return Truncator(value).words(length, truncate="")
