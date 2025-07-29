"""
Context processors for the cart application.

This module provides context processors that inject cart-related variables
into the template context for all templates rendered by the application.
"""
from .models import Cart


def cart_context(request):
    """
    Add cart information to the template context for all templates.
    
    Retrieves the authenticated user's cart item count and makes it
    available to all templates. If the user is not authenticated or
    has no cart, the count is set to zero.
    
    Args:
        request: The HTTP request object
        
    Returns:
        dict: Dictionary containing the cart item count
    """
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = cart.total_items
        except Cart.DoesNotExist:
            cart_count = 0
    
    return {
        'cart_count': cart_count,
    }
    