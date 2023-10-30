"""
Django template module import.

This module provides various utilities for working with Django templates.
"""
from django import template


register = template.Library()


@register.filter
def replace(value, args):
    """
    Custom template filter that replaces occurrences of a search string
    with a replacement string in the given value.

    Args:
        value (str): Original string where replacements will be made.
        args (str): Comma-separated string with the search string and
            replacement string, e.g., "search,replace".

    Returns:
        str: Modified string with replacements.
    """
    search_string, replacement_string = args.split(',')
    return value.replace(search_string, replacement_string)


@register.filter(name='add_index')
def add_index(arr, index):
    """
    Custom template filter that retrieves the element at the specified
    index from a list or iterable.

    Args:
        arr (list or iterable): The list or iterable to retrieve the
            element from.
        index (int): The index of the element to retrieve.

    Returns:
        Any: The element at the specified index in the input list or
        iterable.
    """
    return arr[index]
