from django import template
register = template.Library()

@register.simple_tag
def dictKeyLookup(the_dict, key):
   # Try to fetch from the dict, and if it's not found return an empty string.
   return the_dict.get(key, '')

@register.filter
def get(mapping, key):
  return mapping.get(key, '')

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)