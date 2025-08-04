"""
Django admin configuration for newsletter management.

This module provides administrative interfaces for managing newsletter subscriptions,
allowing staff to monitor subscriber status, manage confirmations, and perform
bulk operations on newsletter data.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """
    Admin interface for managing newsletter subscribers.
    
    Provides a comprehensive admin panel for viewing and managing newsletter
    subscriptions with status indicators, filtering options, and search capabilities.
    Staff can monitor subscription status, confirmation states, and perform
    administrative actions on subscriber data.
    
    Features:
        - Visual status badges for quick subscription state identification
        - Date-based filtering for subscription management
        - Email search functionality
        - Read-only fields for data integrity
    """
    
    list_display = ['email', 'status_badge', 'subscribed_at', 'confirmed_at', 'is_active']
    list_filter = ['is_confirmed', 'is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['confirmation_token', 'subscribed_at', 'confirmed_at']
    
    def status_badge(self, obj):
        """
        Generate a colored status badge for newsletter subscribers.
        
        Creates visual indicators to quickly identify subscriber status:
        - Green checkmark: Active confirmed subscribers
        - Orange pause: Confirmed but unsubscribed users
        - Red hourglass: Pending confirmation
        
        Args:
            obj (NewsletterSubscriber): The subscriber instance to evaluate
            
        Returns:
            str: HTML formatted status badge with appropriate color and icon
            
        Examples:
            Active subscriber: "✅ Active" (green)
            Unsubscribed user: "⏸️ Unsubscribed" (orange)
            Pending confirmation: "⏳ Pending" (red)
        """
        if obj.is_confirmed and obj.is_active:
            return format_html('<span style="color: green;">✅ Active</span>')
        elif obj.is_confirmed and not obj.is_active:
            return format_html('<span style="color: orange;">⏸️ Unsubscribed</span>')
        else:
            return format_html('<span style="color: red;">⏳ Pending</span>')
    
    status_badge.short_description = 'Status'