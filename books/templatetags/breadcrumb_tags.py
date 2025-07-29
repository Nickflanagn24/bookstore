"""
Custom template tags for the accounts application.

This module provides template tags to enhance template functionality,
particularly for displaying book information and breadcrumb navigation.
"""
from django import template
from django.utils.text import capfirst
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def get_book_title(context):
    """
    Extract and return the book title from the template context.
    
    Attempts to find a book title by checking multiple possible context
    variables that might contain book information. Used primarily for
    generating consistent breadcrumb navigation.
    
    Args:
        context: The template context object containing variables
        
    Returns:
        str: The book title if found, or 'Book Details' as a fallback
    """
    # Try different variable names that might contain the book
    book = context.get('book', None)
    if book and hasattr(book, 'title'):
        return book.title
    
    object = context.get('object', None)
    if object and hasattr(object, 'title'):
        return object.title
    
    return "Book Details"
    