"""
Views for the orders application.

This module handles order-related views including order listing, order details,
order creation from cart, and order success confirmation pages.
"""
import logging
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal

from .models import Order, OrderItem
from cart.models import Cart
from books.models import Book

# Configure logging
logger = logging.getLogger(__name__)


@login_required
def order_list(request):
    """
    Display a list of orders for the current user.
    
    Shows all orders belonging to the authenticated user, ordered by
    creation date (most recent first).
    
    Args:
        request: The HTTP request object containing user information.
        
    Returns:
        HttpResponse: Rendered template with user's orders.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'page_title': 'My Orders',
    }
    
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_number):
    """
    Display detailed information about a specific order.
    
    Shows comprehensive order information including items, pricing,
    payment status, and delivery information for orders belonging
    to the authenticated user.
    
    Args:
        request: The HTTP request object containing user information.
        order_number: The unique order number to display.
        
    Returns:
        HttpResponse: Rendered template with order details.
        
    Raises:
        Http404: If order doesn't exist or doesn't belong to the user.
    """
    order = get_object_or_404(
        Order, 
        order_number=order_number, 
        user=request.user
    )
    
    # Get order items with book details
    order_items = order.items.select_related('book').all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'page_title': f'Order {order.order_number}',
    }
    
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_success(request, order_number):
    """
    Display order confirmation success page.
    
    Shows a confirmation page after successful payment processing,
    including order summary and next steps information.
    
    Args:
        request: The HTTP request object containing user information.
        order_number: The unique order number for the successful order.
        
    Returns:
        HttpResponse: Rendered success template with order confirmation.
        
    Raises:
        Http404: If order doesn't exist or doesn't belong to the user.
    """
    order = get_object_or_404(
        Order, 
        order_number=order_number, 
        user=request.user
    )
    
    # Get order items with book details
    order_items = order.items.select_related('book').all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'page_title': 'Order Confirmation',
        'is_success_page': True,
    }
    
    return render(request, 'orders/order_success.html', context)


@login_required
@require_POST
def create_order_from_cart(request):
    """
    Create a new order from the user's cart contents.
    
    This view handles the creation of orders from cart items,
    typically used for alternative checkout flows or manual
    order processing.
    
    Args:
        request: The HTTP request object containing user and cart data.
        
    Returns:
        JsonResponse: JSON response indicating success/failure with
                     order details or error messages.
    """
    try:
        # Get user's cart
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            return JsonResponse({
                'success': False,
                'error': 'Your cart is empty.'
            })
        
        # Calculate total
        total = sum(
            item.book.price * item.quantity for item in cart_items
        )
        
        # Add shipping
        shipping = Decimal('5.00')
        total_with_shipping = total + shipping
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_with_shipping,
            status='pending',
            payment_status='pending',
            customer_email=request.user.email,
            customer_first_name=request.user.first_name or '',
            customer_last_name=request.user.last_name or '',
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.price
            )
        
        # Clear cart
        cart_items.delete()
        
        logger.info(f"Order {order.order_number} created from cart for user {request.user.id}")
        
        return JsonResponse({
            'success': True,
            'order_id': str(order.id),
            'order_number': order.order_number,
            'redirect_url': order.get_absolute_url()
        })
        
    except Exception as e:
        logger.error(f"Error creating order from cart: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to create order. Please try again.'
        })
        