# __init__.py
from django import template
from .custom_filters import *

register = template.Library()
