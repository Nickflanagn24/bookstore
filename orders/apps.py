"""
Django app configuration for the orders application.

This module defines the application configuration for the orders app,
specifying the auto field type and application name.
"""
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Application configuration class for the orders app.
    
    This class configures Django's application registry with settings
    specific to the orders application, such as the default auto field
    and application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
    