# -*- coding: utf-8 -*-
from django import template

__author__ = 'sungjinyoo'

register = template.Library()

@register.filter
def nth(list, index):
    return list[index]