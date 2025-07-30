"""
URL configuration for the orders application.

This module defines URL patterns for order-related views, including order listing,
order details, order creation, and success pages.
"""
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<str:order_number>/', views.order_detail, name='order_detail'),
    path('<str:order_number>/success/', views.order_success, name='order_success'),
    path('create-from-cart/', views.create_order_from_cart, name='create_order_from_cart'),
]
