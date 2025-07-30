"""
Checkout views for the Django bookstore application.

This module handles the checkout process, including payment processing
with Stripe integration and order creation functionality.
"""

import json
import logging
import stripe
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from cart.models import Cart
from orders.models import Order, OrderItem
from books.models import Book


# Configure logging
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def hardwired_checkout(request):
    """
    Display the hardwired checkout page with Stripe payment integration.
    
    This view handles the display of the checkout form with all necessary
    context for payment processing, including cart items, total amount,
    and Stripe configuration.
    
    Args:
        request: The HTTP request object containing user and session data.
        
    Returns:
        HttpResponse: Rendered checkout template with payment context.
        
    Raises:
        Http404: If user's cart is not found or is empty.
    """
    try:
        # Get user's cart
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:cart_detail')
        
        # Calculate totals
        subtotal = sum(
            item.book.price * item.quantity for item in cart_items
        )
        shipping = Decimal('5.00')  # Fixed shipping cost
        total = subtotal + shipping
        
        # Convert to pence for Stripe (multiply by 100)
        stripe_total = int(total * 100)
        
        logger.info(
            f"Checkout initiated for user {request.user.id}. "
            f"Total: £{total}, Stripe amount: {stripe_total}p"
        )
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'stripe_total': stripe_total,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        
        return render(request, 'hardwired_checkout.html', context)
        
    except Exception as e:
        logger.error(f"Error in hardwired_checkout view: {str(e)}")
        messages.error(
            request, 
            'An error occurred while loading the checkout page. '
            'Please try again.'
        )
        return redirect('cart:cart_detail')


@login_required
@require_POST
def process_hardwired_payment(request):
    """
    Process the Stripe payment and create order.
    
    This view handles the server-side payment processing using Stripe's
    Payment Intent API, creates the order upon successful payment,
    and clears the user's cart.
    
    Args:
        request: The HTTP request object containing payment data.
        
    Returns:
        JsonResponse: JSON response indicating success or failure with
                     appropriate error messages.
    """
    try:
        # Get user's cart
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items.exists():
            logger.warning(f"Empty cart for user {request.user.id}")
            return JsonResponse({
                'success': False,
                'error': 'Your cart is empty.'
            })
        
        # Calculate totals
        subtotal = sum(
            item.book.price * item.quantity for item in cart_items
        )
        shipping = Decimal('5.00')
        total = subtotal + shipping
        stripe_total = int(total * 100)  # Convert to pence
        
        # Get payment method ID from request
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        
        if not payment_method_id:
            logger.error("No payment method ID provided")
            return JsonResponse({
                'success': False,
                'error': 'Payment method is required.'
            })
        
        logger.info(
            f"Processing payment for user {request.user.id}. "
            f"Amount: {stripe_total}p, Payment method: {payment_method_id}"
        )
        
        # Create payment intent with Stripe
        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency='gbp',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url=request.build_absolute_uri('/orders/success/'),
                metadata={
                    'user_id': request.user.id,
                    'user_email': request.user.email,
                }
            )
            
            logger.info(
                f"Stripe PaymentIntent created: {intent.id}, "
                f"Status: {intent.status}"
            )
            
        except stripe.error.CardError as e:
            logger.error(f"Stripe card error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Card error: {e.user_message}'
            })
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Payment processing error. Please try again.'
            })
        
        # Handle payment intent status
        if intent.status == 'requires_action':
            logger.info(f"Payment requires action: {intent.id}")
            return JsonResponse({
                'success': False,
                'requires_action': True,
                'payment_intent': {
                    'id': intent.id,
                    'client_secret': intent.client_secret
                }
            })
        elif intent.status == 'succeeded':
            logger.info(f"Payment succeeded: {intent.id}")
            
            # Create order with correct field names
            try:
                order = Order.objects.create(
                    user=request.user,
                    stripe_payment_intent_id=intent.id,  # Correct field name
                    total_amount=total,
                    status='confirmed',  # Valid status from your choices
                    payment_status='paid',  # Set payment status
                    customer_email=request.user.email,
                    customer_first_name=request.user.first_name or '',
                    customer_last_name=request.user.last_name or '',
                )
                
                # Create order items - let the save() method handle book details
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        book=cart_item.book,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.book.price
                    )
                
                # Clear cart
                cart_items.delete()
                
                logger.info(
                    f"Order created successfully: {order.id} "
                    f"for user {request.user.id}"
                )
                
                return JsonResponse({
                    'success': True,
                    'order_id': str(order.id),
                    'order_number': order.order_number,
                    'redirect_url': f'/orders/{order.order_number}/success/'
                })
                
            except Exception as e:
                logger.error(f"Error creating order: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': 'Order creation failed. Please contact support.'
                })
        else:
            logger.error(f"Unexpected payment status: {intent.status}")
            return JsonResponse({
                'success': False,
                'error': f'Payment failed with status: {intent.status}'
            })
            
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({
            'success': False,
            'error': 'Invalid request data.'
        })
    except Exception as e:
        logger.error(f"Unexpected error in payment processing: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred. Please try again.'
        })


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Handle Stripe webhook events.
    
    This view processes webhook events from Stripe to handle various
    payment-related events and update order statuses accordingly.
    
    Args:
        request: The HTTP request object containing webhook data.
        
    Returns:
        JsonResponse: Acknowledgment response for Stripe webhook.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    
    if not endpoint_secret:
        logger.warning("STRIPE_WEBHOOK_SECRET not configured")
        return JsonResponse({'error': 'Webhook not configured'}, status=400)
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        logger.info(f"Stripe webhook received: {event['type']}")
        
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.info(f"Payment succeeded: {payment_intent['id']}")
        
        # Update order status if needed
        try:
            order = Order.objects.get(
                stripe_payment_intent_id=payment_intent['id']  # Correct field name
            )
            if order.payment_status != 'paid':
                order.payment_status = 'paid'
                order.status = 'confirmed'
                order.save()
                logger.info(f"Order {order.id} status updated to paid")
        except Order.DoesNotExist:
            logger.warning(
                f"Order not found for payment intent: {payment_intent['id']}"
            )
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logger.warning(f"Payment failed: {payment_intent['id']}")
        
        # Update order status
        try:
            order = Order.objects.get(
                stripe_payment_intent_id=payment_intent['id']  # Correct field name
            )
            order.payment_status = 'failed'
            order.status = 'cancelled'
            order.save()
            logger.info(f"Order {order.id} status updated to failed")
        except Order.DoesNotExist:
            logger.warning(
                f"Order not found for failed payment: {payment_intent['id']}"
            )
    
    else:
        logger.info(f"Unhandled event type: {event['type']}")
    
    return JsonResponse({'status': 'success'})