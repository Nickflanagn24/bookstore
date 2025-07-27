from django.urls import resolve, reverse
from django.utils.text import capfirst

def breadcrumbs(request):
    """
    Context processor for generating breadcrumbs based on the current URL
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
