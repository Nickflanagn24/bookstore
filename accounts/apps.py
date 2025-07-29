"""
Django app configuration for the accounts application.

This module defines the application configuration for the accounts app,
specifying the auto field type and application name.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Application configuration class for the accounts app.
    
    This class configures Django's application registry with settings
    specific to the accounts application, such as the default auto field
    and application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    