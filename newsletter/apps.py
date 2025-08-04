"""
Django application configuration for the newsletter app.

This module defines configuration settings for the Tales & Tails bookstore
newsletter application, handling customer email subscriptions and management.
"""

from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    """
    Configuration class for the newsletter Django application.
    
    Defines application settings and metadata for newsletter functionality
    within the Tales & Tails bookstore system. Manages customer email
    subscriptions, double opt-in confirmations, and preference handling.
    
    The newsletter app provides:
        - Customer email subscription management
        - Double opt-in confirmation system
        - Subscription status tracking
        - Email preference management
        - Admin interface for newsletter oversight
    
    Attributes:
        default_auto_field (str): Specifies the default primary key field type
            for models in this app. Uses BigAutoField for scalability.
        name (str): The Python path to the application module, used by Django
            for app discovery and registration.
    
    Usage:
        This class is automatically discovered by Django when the 'newsletter'
        app is included in the INSTALLED_APPS setting.
        
    Example:
        In settings.py:
        INSTALLED_APPS = [
            ...
            'newsletter',  # This triggers NewsletterConfig loading
            ...
        ]
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'