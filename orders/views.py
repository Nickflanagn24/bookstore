from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Order, OrderItem
from cart.models import Cart
from books.models import Book

@login_required
def order_list(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items__book')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)

@login_required
def order_detail(request, order_number):
    """Display detailed order information"""
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
    """Create an order from the user's current cart"""
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
        
        # Send order confirmation email
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        from django.conf import settings
        
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
                subject=f"Tales & Tails - Order Confirmation #{order.order_number}",
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.customer_email],
                html_message=html_message,
                fail_silently=True,
            )
            print(f"✅ Order confirmation email sent to {order.customer_email}")
        except Exception as e:
            print(f"❌ Failed to send order confirmation email: {e}")
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
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

def confirm_order_from_stripe(stripe_session_id, payment_intent_id=None):
    """
    Utility function to confirm order after successful Stripe payment
    This will be called from the cart checkout views
    """
    try:
        # Find the order by stripe session ID or create if needed
        # This function will be integrated with your existing Stripe checkout
        pass
    except Exception as e:
        print(f"Error confirming order: {e}")
        return None
