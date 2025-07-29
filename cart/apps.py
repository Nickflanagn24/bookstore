"""
Django app configuration for the shopping cart application.

This module defines the application configuration for the cart app,
specifying the auto field type and application name.
"""
from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Application configuration class for the cart app.
    
    This class configures Django's application registry with settings
    specific to the cart application, such as the default auto field
    and application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"
