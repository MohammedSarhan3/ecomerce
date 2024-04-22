# Create a templatetags directory in your app and add __init__.py file
# Then, create a custom_filters.py file in the templatetags directory.

# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_subcategory_name')
def get_subcategory_name(subcategories, subcategory_id):
    try:
        subcategory = subcategories.get(Subcategory_id=subcategory_id)
        return subcategory.Name
    except Subcategory.DoesNotExist:
        return 'No Subcategory'

@register.filter(name='get_subcategory_id')
def get_subcategory_id(subcategories, subcategory_id):
    try:
        subcategory = subcategories.get(Subcategory_id=subcategory_id)
        return subcategory.Subcategory_id
    except Subcategory.DoesNotExist:
        return 'No Subcategory'
