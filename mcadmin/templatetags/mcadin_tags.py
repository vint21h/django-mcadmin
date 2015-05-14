# -*- coding: utf-8 -*-

# django-mcadmin
# mcadmin/templatetags/mcadmin_tags.py

from django import template

__all__ = ['get', 'pop', ]


register = template.Library()

@register.filter()
def get(d, key):
    """
    Return key value from dict by key.
    """

    return d.get(key, None)

@register.filter()
def pop(d, key):
    """
    pop key value from dict.
    """

    return d.pop(key, None)
