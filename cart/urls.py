"""
URL configuration for the cart application.

This module defines URL patterns for cart-related views, including cart management,
checkout processes, and payment handling through Stripe integration.
"""
from django.urls import path
from . import views
from . import checkout_views


app_name = 'cart'

urlpatterns = [
    # Cart management URLs
    path('', views.cart_detail, name='cart_detail'),
    path('add/<uuid:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<uuid:item_id>/', views.update_cart_item, name='update_item'),
    path('remove/<uuid:item_id>/', views.remove_from_cart, name='remove_item'),
    path('clear/', views.clear_cart, name='clear_cart'),
    
    # Checkout URLs
    path('checkout/', checkout_views.checkout, name='checkout'),
    path(
        'checkout/create-session/',
        checkout_views.create_checkout_session,
        name='create_checkout_session'
    ),
    path(
        'checkout/success/',
        checkout_views.checkout_success,
        name='checkout_success'
    ),
    path(
        'checkout/cancelled/',
        checkout_views.checkout_cancelled,
        name='checkout_cancelled'
    ),
    path(
        'stripe/webhook/',
        checkout_views.stripe_webhook,
        name='stripe_webhook'
    ),
    
    # Professional Secure Checkout URLs
    path(
        "secure-checkout/",
        checkout_views.hardwired_checkout,
        name="secure_checkout"
    ),
    path(
        "process-secure-payment/",
        checkout_views.process_hardwired_payment,
        name="process_secure_payment"
    ),
]
