"""
Email notification functions for the orders application.

This module provides functions for sending order-related email notifications,
such as order confirmations and shipping notifications.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    """
    Send order confirmation email to the customer.
    
    Generates and sends an order confirmation email with order details
    in both plain text and HTML formats (if a template exists).
    
    Args:
        order: The Order object with customer and order information
        
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    if not order.user or not order.user.email:
        return False
    
    # Build the order URL
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    order_url = f"{site_url}{reverse('orders:order_detail', kwargs={'pk': order.id})}"
    
    context = {
        'order': order,
        'order_url': order_url,
        'contact_email': settings.DEFAULT_FROM_EMAIL,
    }
    
    # Create the email
    subject = f'Tales & Tails - Order Confirmation #{order.id}'
    
    # Plain text version
    text_content = f"""
Order Confirmation #{order.id}

Dear {order.user.first_name if order.user.first_name else 'Valued Customer'},

Thank you for your order from Tales & Tails. We're processing your order and will notify you when it ships.

Order Details:
- Order Number: {order.id}
- Order Date: {order.created_at.strftime('%B %d, %Y')}

View your order details at: {order_url}

If you have any questions about your order, please contact our customer service team.

Thank you for shopping with Tales & Tails!
    """
    
    # HTML version
    try:
        html_content = render_to_string('emails/order_confirmation.html', context)
    except Exception as e:
        logger.error(f"Error rendering HTML template: {str(e)}")
        html_content = None
    
    # Send email
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send()
        return True
    except Exception as e:
        logger.error(f"Error sending order confirmation: {str(e)}")
        return False


def send_shipping_notification(order):
    """
    Send shipping notification email to the customer.
    
    Generates and sends an email notifying the customer that their order
    has been shipped, including tracking information if available.
    
    Args:
        order: The Order object with shipping and customer information
        
    Returns:
        bool: True if the email was sent successfully, False otherwise
    """
    if not order.user or not order.user.email:
        return False
    
    # Build the order URL
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    order_url = f"{site_url}{reverse('orders:order_detail', kwargs={'pk': order.id})}"
    
    # Build the tracking URL if tracking number exists
    tracking_url = None
    if hasattr(order, 'tracking_number') and order.tracking_number:
        # This is a simple example - you might need to use specific carrier APIs
        tracking_url = (
            f"https://www.royalmail.com/track-your-item#/tracking-results/"
            f"{order.tracking_number}"
        )
    
    context = {
        'order': order,
        'order_url': order_url,
        'tracking_url': tracking_url,
        'contact_email': settings.DEFAULT_FROM_EMAIL,
    }
    
    # Create the email
    subject = f'Tales & Tails - Your Order #{order.id} Has Shipped!'
    
    # Plain text version
    shipping_date_str = (
        order.shipping_date.strftime('%B %d, %Y')
        if hasattr(order, 'shipping_date') else 'N/A'
    )
    
    tracking_info = (
        f"- Tracking Number: {order.tracking_number}"
        if hasattr(order, 'tracking_number') and order.tracking_number
        else ""
    )
    
    text_content = f"""
Your Order Has Shipped!

Dear {order.user.first_name if order.user.first_name else 'Valued Customer'},

Great news! Your order from Tales & Tails has been shipped and is on its way to you.

Shipping Details:
- Order Number: {order.id}
- Shipping Date: {shipping_date_str}
{tracking_info}

View your order details at: {order_url}

If you have any questions about your shipment, please contact our customer service team.

We hope you enjoy your books!
    """
    
    # HTML version
    try:
        html_content = render_to_string('emails/shipping_notification.html', context)
    except Exception as e:
        logger.error(f"Error rendering HTML template: {str(e)}")
        html_content = None
    
    # Send email
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send()
        return True
    except Exception as e:
        logger.error(f"Error sending shipping notification: {str(e)}")
        return False
        