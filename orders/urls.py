"""
URL configuration for the orders application.

This module defines URL patterns for order-related views, including order listing,
order details, and order creation from cart contents.
"""
from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    # Order management URLs
    path('', views.order_list, name='order_list'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
    path(
        'create-from-cart/',
        views.create_order_from_cart,
        name='create_order_from_cart'
    ),
]
