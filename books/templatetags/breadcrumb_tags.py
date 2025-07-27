from django import template
from django.utils.text import capfirst
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def get_book_title(context):
    """Get the book title from the context for breadcrumbs"""
    # Try different variable names that might contain the book
    book = context.get('book', None)
    if book and hasattr(book, 'title'):
        return book.title
    
    object = context.get('object', None)
    if object and hasattr(object, 'title'):
        return object.title
    
    return "Book Details"
