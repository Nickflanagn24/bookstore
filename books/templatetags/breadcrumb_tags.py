from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    """Generate breadcrumbs based on current URL and context"""
    request = context['request']
    url_name = request.resolver_match.url_name
    namespace = request.resolver_match.namespace
    
    # Base breadcrumb structure
    breadcrumbs = [{'name': 'Home', 'url': reverse('books:book_list')}]
    
    # Add breadcrumbs based on current page
    if namespace == 'books':
        if url_name == 'book_list':
            breadcrumbs.append({'name': 'Books', 'url': None})
            
        elif url_name == 'book_detail':
            book = context.get('book')
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': book.title[:30] + '...' if len(book.title) > 30 else book.title, 'url': None}
            ])
            
        elif url_name == 'category_detail':
            category = context.get('category')
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': f'Category: {category.name}', 'url': None}
            ])
            
        elif url_name == 'author_detail':
            author = context.get('author')
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': f'Author: {author.name}', 'url': None}
            ])
            
        elif url_name == 'about':
            breadcrumbs.append({'name': 'About Us', 'url': None})
            
        elif url_name == 'contact':
            breadcrumbs.append({'name': 'Contact', 'url': None})
            
        elif url_name == 'book_manage':
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': 'Manage Books', 'url': None}
            ])
            
        elif url_name == 'book_create':
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': 'Manage Books', 'url': reverse('books:book_manage')},
                {'name': 'Add New Book', 'url': None}
            ])
            
        elif url_name == 'book_edit':
            book = context.get('book')
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': 'Manage Books', 'url': reverse('books:book_manage')},
                {'name': f'Edit: {book.title[:20]}...', 'url': None}
            ])
            
        elif url_name == 'review_create':
            book = context.get('book')
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': book.title[:20] + '...', 'url': reverse('books:book_detail', args=[book.id])},
                {'name': 'Write Review', 'url': None}
            ])
            
        elif url_name == 'review_edit':
            review = context.get('review')
            if review:
                breadcrumbs.extend([
                    {'name': 'Books', 'url': reverse('books:book_list')},
                    {'name': review.book.title[:20] + '...', 'url': reverse('books:book_detail', args=[review.book.id])},
                    {'name': 'Edit Review', 'url': None}
                ])
                
        elif url_name == 'user_reviews':
            breadcrumbs.extend([
                {'name': 'Books', 'url': reverse('books:book_list')},
                {'name': 'My Reviews', 'url': None}
            ])
    
    elif namespace == 'accounts':
        if url_name == 'profile':
            breadcrumbs.append({'name': 'My Profile', 'url': None})
        elif url_name == 'login':
            breadcrumbs.append({'name': 'Login', 'url': None})
        elif url_name == 'signup':
            breadcrumbs.append({'name': 'Sign Up', 'url': None})
            
    elif namespace == 'cart':
        if url_name == 'cart_detail':
            breadcrumbs.append({'name': 'Shopping Cart', 'url': None})
        elif url_name == 'checkout':
            breadcrumbs.extend([
                {'name': 'Shopping Cart', 'url': reverse('cart:cart_detail')},
                {'name': 'Checkout', 'url': None}
            ])
    
    return breadcrumbs
