"""
Django app configuration for the books application.

This module defines the application configuration for the books app,
specifying the auto field type and application name.
"""
from django.apps import AppConfig


class BooksConfig(AppConfig):
    """
    Application configuration class for the books app.
    
    This class configures Django's application registry with settings
    specific to the books application, such as the default auto field
    and application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "books"
    