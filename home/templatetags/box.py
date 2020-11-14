#-*-coding:utf-8 -*-
from django import template

register = template.Library()

@register.filter
def set_password(value):
    return "*"*10

@register.filter
def set_content(value):
    if len(value)>10:
        return value[0:10]+"..."
    return value