"""
Django app configuration for the pages application.

This module defines the application configuration for the pages app,
specifying the auto field type and application name.
"""
from django.apps import AppConfig


class PagesConfig(AppConfig):
    """
    Application configuration class for the pages app.
    
    This class configures Django's application registry with settings
    specific to the pages application, such as the default auto field
    and application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"
    