"""
Context processors for the books application.

This module provides context processors that inject additional variables
into the template context, such as navigation breadcrumbs.
"""
from django.urls import resolve, reverse
from django.utils.text import capfirst


def breadcrumbs(request):
    """
    Generate navigation breadcrumbs based on the current URL path.
    
    Creates a hierarchical trail of links representing the path from
    the site root to the current page, parsing URL segments to create
    human-readable titles and appropriate links.
    
    Args:
        request: The HTTP request object containing the current path
        
    Returns:
        dict: A dictionary with a 'breadcrumb_items' key containing a list
            of dictionaries, each with 'title' and 'url' keys (url is None
            for the current page)
    """
    path = request.path.strip('/')
    parts = path.split('/')
    breadcrumb_items = []
    
    # Build up the URL as we go
    current_url = ''
    app_name = None
    
    for i, part in enumerate(parts):
        if not part:  # Skip empty parts
            continue
            
        current_url += '/' + part
        
        # Try to get a readable name for this URL part
        if i == 0:
            # This is likely an app name
            app_name = part
            title = capfirst(part.replace('-', ' '))
        else:
            # This could be an object ID or slug
            title = capfirst(part.replace('-', ' '))
        
        # For the last part (current page), we don't include a URL
        if i == len(parts) - 1:
            breadcrumb_items.append({'title': title, 'url': None})
        else:
            breadcrumb_items.append({'title': title, 'url': current_url})
    
    return {'breadcrumb_items': breadcrumb_items}
