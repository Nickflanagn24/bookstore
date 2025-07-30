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
    path('checkout/', checkout_views.hardwired_checkout, name='checkout'),
    path(
        'process-payment/',
        checkout_views.process_hardwired_payment,
        name='process_hardwired_payment'
    ),
    path(
        'stripe/webhook/',
        checkout_views.stripe_webhook,
        name='stripe_webhook'
    ),
]
