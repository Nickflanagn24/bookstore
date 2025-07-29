"""
View functions for the orders application.

This module provides Django view functions for order management, including
viewing order history, displaying order details, and creating orders from cart.
"""
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

from books.models import Book
from cart.models import Cart
from .models import Order, OrderItem


logger = logging.getLogger(__name__)


@login_required
def order_list(request):
    """
    Display user's order history.
    
    Retrieves and displays all orders for the authenticated user
    with optimised database queries using prefetch_related.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered order list template with orders context
    """
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items__book')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_number):
    """
    Display detailed order information.
    
    Shows comprehensive information about a specific order, including
    all items, status history, and customer details.
    
    Args:
        request: The HTTP request object
        order_number: The unique order number to look up
        
    Returns:
        Rendered order detail template with order context
    """
    order = get_object_or_404(
        Order.objects.prefetch_related('items__book', 'status_history'),
        order_number=order_number,
        user=request.user
    )
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
@require_POST
def create_order_from_cart(request):
    """
    Create an order from the user's current cart.
    
    Converts the current cart contents into an order, sends a confirmation
    email to the customer, and clears the cart. Returns JSON response
    for AJAX handling.
    
    Args:
        request: The HTTP request object
        
    Returns:
        JsonResponse with order details or error information
    """
    try:
        cart = Cart.objects.get(user=request.user)
        
        if cart.is_empty:
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty'
            }, status=400)
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            customer_email=request.user.email,
            customer_first_name=request.user.first_name,
            customer_last_name=request.user.last_name,
            status='pending'
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.price
            )
        
        # Prepare email
        context = {
            "order": order,
            "site_url": request.build_absolute_uri("/").rstrip("/"),
        }
        html_message = render_to_string("emails/order_confirmation.html", context)
        plain_message = strip_tags(html_message)
        
        # Send email
        try:
            send_mail(
                subject=(
                    f"Tales & Tails - Order Confirmation #{order.order_number}"
                ),
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.customer_email],
                html_message=html_message,
                fail_silently=True,
            )
            logger.info(
                f"Order confirmation email sent to {order.customer_email}"
            )
        except Exception as e:
            logger.error(f"Failed to send order confirmation email: {e}")
            
        # Clear the cart
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'order_url': order.get_absolute_url()
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Cart not found'
        }, status=404)
    except Exception as e:
        logger.error(f"Error creating order from cart: {e}")
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def confirm_order_from_stripe(stripe_session_id, payment_intent_id=None):
    """
    Confirm order after successful Stripe payment.
    
    Utility function to update order status after receiving successful
    payment confirmation from Stripe. This function is called from
    cart checkout views.
    
    Args:
        stripe_session_id: The Stripe session ID linked to the order
        payment_intent_id: Optional Stripe payment intent ID
        
    Returns:
        Order object if successful, None on error
    """
    try:
        # Find the order by stripe session ID or create if needed
        # This function will be integrated with your existing Stripe checkout
        pass
    except Exception as e:
        logger.error(f"Error confirming order: {e}")
        return None
        