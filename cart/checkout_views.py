"""
Stripe integration and checkout functionality for the cart application.

This module handles payment processing with Stripe, including checkout sessions,
payment verification, webhooks, and order management for completed payments.
"""
import json
import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Cart, CartItem
from orders.models import Order, OrderItem, OrderStatusHistory


# Configure Stripe with our secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


@login_required
def checkout(request):
    """
    Display checkout page with cart items and Stripe integration.
    
    Retrieves the user's active cart and prepares the checkout page with
    cart items, total price, and Stripe payment configuration.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered checkout page or redirect to cart if empty
    """
    try:
        # Get user's cart or redirect if empty
        cart = Cart.objects.get(user=request.user)
        if cart.is_empty:
            messages.info(request, "Your cart is empty!")
            return redirect('cart:cart_detail')
        
        # Prepare context for checkout template
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related('book').all(),
            'total_amount': int(cart.total_price * 100),  # Convert to cents for Stripe
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, 'cart/checkout.html', context)
        
    except Cart.DoesNotExist:
        # Handle case where user has no cart
        messages.info(request, "Your cart is empty!")
        return redirect('cart:cart_detail')


@login_required
@require_POST
def create_checkout_session(request):
    """
    Create a Stripe checkout session for payment processing.
    
    Generates a Stripe checkout session with the items from the user's cart,
    creates a pending order in the database, and returns the checkout URL
    for the client to redirect to.
    
    Args:
        request: The HTTP request object
        
    Returns:
        JsonResponse with checkout URL or error message
    """
    try:
        # Get user's cart and validate it's not empty
        cart = Cart.objects.get(user=request.user)
        
        if cart.is_empty:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Create order BEFORE Stripe checkout
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            customer_email=request.user.email,
            customer_first_name=request.user.first_name or 'Customer',
            customer_last_name=request.user.last_name or 'User',
            status='pending',
            payment_status='pending'
        )
        
        # Create order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.price
            )
        
        # Build line items for Stripe from cart contents
        line_items = []
        for item in cart.items.all():
            image_urls = []
            if item.book.cover_image or item.book.thumbnail:
                image_urls = [item.book.cover_image or item.book.thumbnail]
                
            line_items.append({
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {
                        'name': item.book.title,
                        'description': f"by {item.book.authors_list}",
                        'images': image_urls,
                    },
                    'unit_amount': int(item.book.price * 100),  # Stripe requires cents
                },
                'quantity': item.quantity,
            })
        
        # Create the Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # Accept card payments
            line_items=line_items,
            mode='payment',  # One-time payment
            customer_email=request.user.email,
            # Set success and cancel URLs
            success_url=(
                request.build_absolute_uri('/cart/checkout/success/') +
                '?session_id={CHECKOUT_SESSION_ID}'
            ),
            cancel_url=request.build_absolute_uri('/cart/checkout/cancelled/'),
            # Store user, cart, and ORDER info for later reference
            metadata={
                'user_id': str(request.user.id),
                'cart_id': str(cart.id),
                'order_id': str(order.id),  # Important: link to our order
                'order_number': order.order_number,
            }
        )
        
        # Update order with Stripe session ID
        order.stripe_session_id = checkout_session.id
        order.save()
        
        # Return the checkout URL to frontend
        return JsonResponse({'checkout_url': checkout_session.url})
        
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=404)
    except Exception as e:
        # Log errors for debugging
        logger.error(f"Error creating checkout session: {str(e)}")
        return JsonResponse(
            {'error': 'Unable to create checkout session'},
            status=500
        )


@login_required
def checkout_success(request):
    """
    Handle successful payment confirmation.
    
    Verifies payment with Stripe, updates the order status to confirmed,
    clears the user's cart, and displays a success message.
    
    Args:
        request: The HTTP request object with session_id parameter
        
    Returns:
        Rendered success page or redirect with error message
    """
    session_id = request.GET.get('session_id')
    
    if session_id:
        try:
            # Verify payment with Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Only proceed if payment was actually completed
            if session.payment_status == 'paid':
                # Find and confirm the order
                try:
                    order = Order.objects.get(stripe_session_id=session_id)
                    
                    # Update order status
                    old_status = order.status
                    order.status = 'confirmed'
                    order.payment_status = 'paid'
                    order.confirmed_at = timezone.now()
                    order.stripe_payment_intent_id = session.payment_intent
                    order.save()
                    
                    # Record status change
                    OrderStatusHistory.objects.create(
                        order=order,
                        from_status=old_status,
                        to_status='confirmed',
                        notes='Payment confirmed via Stripe',
                    )
                    
                    # Clear the user's cart since payment succeeded
                    try:
                        cart = Cart.objects.get(user=request.user)
                        cart.items.all().delete()  # Remove all cart items
                    except Cart.DoesNotExist:
                        pass  # Cart already cleared or doesn't exist
                    
                    success_msg = (
                        f"✅ Payment successful! Your order {order.order_number} "
                        f"has been confirmed."
                    )
                    messages.success(request, success_msg)
                    
                    # Prepare success page context
                    context = {
                        'order': order,
                        'session': session,
                        'customer_email': session.customer_email,
                        # Convert cents back to pounds
                        'amount_total': session.amount_total / 100,
                    }
                    return render(request, 'cart/checkout_success.html', context)
                    
                except Order.DoesNotExist:
                    logger.error(f"Order not found for session: {session_id}")
                    messages.error(
                        request,
                        "Order not found. Please contact support."
                    )
                    return redirect('cart:cart_detail')
        
        except stripe.error.StripeError as e:
            # Handle Stripe API errors
            logger.error(f"Stripe error: {str(e)}")
            messages.error(request, "There was an issue verifying your payment.")
    
    # If we get here, something went wrong
    messages.error(request, "Payment verification failed.")
    return redirect('cart:cart_detail')


@login_required
def checkout_cancelled(request):
    """
    Handle when user cancels payment.
    
    Displays a message indicating the payment was cancelled and
    redirects the user back to their cart.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Redirect to cart detail page with informational message
    """
    messages.info(request, "Payment was cancelled. Your cart is still available.")
    return redirect('cart:cart_detail')


@csrf_exempt
def stripe_webhook(request):
    """
    Handle incoming webhooks from Stripe for payment events.
    
    Processes webhook events from Stripe, verifies the signature,
    and updates orders based on payment status changes.
    
    Args:
        request: The HTTP request object containing webhook data
        
    Returns:
        HttpResponse with appropriate status code
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_ENDPOINT_SECRET', '')
    
    try:
        # Verify webhook signature for security
        if endpoint_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        else:
            # If no webhook secret configured, parse directly (less secure)
            event = json.loads(payload)
    except ValueError:
        # Invalid payload
        logger.error("Invalid payload in webhook")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        logger.error("Invalid signature in webhook")
        return HttpResponse(status=400)
    
    # Process different webhook events
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session['id']
        
        logger.info(f"Payment successful for session: {session_id}")
        
        # Update order status if not already done
        try:
            order = Order.objects.get(stripe_session_id=session_id)
            if order.status == 'pending':
                order.status = 'confirmed'
                order.payment_status = 'paid'
                order.confirmed_at = timezone.now()
                order.save()
                
                # Record status change
                OrderStatusHistory.objects.create(
                    order=order,
                    from_status='pending',
                    to_status='confirmed',
                    notes='Payment confirmed via webhook',
                )
                
                logger.info(f"Order {order.order_number} confirmed via webhook")
        except Order.DoesNotExist:
            logger.error(f"Order not found for webhook session: {session_id}")
        
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logger.info(f"Payment succeeded: {payment_intent['id']}")
    
    else:
        # Log unhandled events for debugging
        logger.info(f"Unhandled event type: {event['type']}")
    
    return HttpResponse(status=200)


@login_required
def hardwired_checkout(request):
    """
    Display hardwired Stripe checkout with custom form.
    
    Shows a custom checkout page that uses Stripe Elements for direct
    integration with the payment form in the page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered hardwired checkout page or redirect with error message
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to proceed with checkout.')
        return redirect('accounts:login')
    
    # Get user's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    if cart.is_empty:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    # Calculate totals
    cart_total = cart.total_price
    cart_total_cents = int(cart_total * 100)  # Stripe uses cents
    
    # Get cart items for display
    cart_items = []
    for item in cart.items.all():
        cart_items.append({
            'book': item.book,
            'quantity': item.quantity,
            'total_price': item.total_price
        })
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_total_cents': cart_total_cents,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, 'hardwired_checkout.html', context)


@csrf_exempt
def process_hardwired_payment(request):
    """
    Process hardwired payment with Payment Intents.
    
    Handles direct payment processing using Stripe Payment Intents API,
    creates an order when payment succeeds, and clears the cart.
    
    Args:
        request: The HTTP POST request with payment data
        
    Returns:
        JsonResponse indicating success or failure
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_method_id = data['payment_method_id']
            amount = data['amount']
            billing_details = data.get('billing_details', {})

            # Get user's cart
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Cart not found.'
                })

            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='gbp',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                metadata={
                    'user_id': (
                        request.user.id if request.user.is_authenticated else None
                    ),
                    'integration_type': 'hardwired'
                }
            )

            if intent.status == 'succeeded':
                # Create order
                order = Order.objects.create(
                    user=(
                        request.user if request.user.is_authenticated else None
                    ),
                    email=billing_details.get('email', ''),
                    total_amount=Decimal(amount) / 100,
                    stripe_payment_intent_id=intent.id,
                    payment_status='completed'
                )
                
                # Add order items from cart
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        book=cart_item.book,
                        quantity=cart_item.quantity,
                        price=cart_item.book.price
                    )
                
                # Clear cart by deleting cart items
                cart.items.all().delete()
                
                # Store order ID in session
                request.session['order_id'] = str(order.id)
                
                return JsonResponse({
                    'success': True,
                    'order_id': str(order.id)
                })

        except stripe.error.CardError as e:
            return JsonResponse({
                'success': False,
                'error': e.user_message or 'Your card was declined.'
            })
        except Exception as e:
            logger.error(f"Payment processing error: {e}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred processing your payment.'
            })

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
    