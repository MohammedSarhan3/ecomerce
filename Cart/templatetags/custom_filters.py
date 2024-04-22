# custom_filters.py
from django import template
from models import get_payment_type

register = template.Library()

@register.filter
def get_payment_type_filter(payment_instance):
    return get_payment_type(payment_instance)
