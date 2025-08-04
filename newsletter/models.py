"""
Django models for newsletter subscription management.

Database models for handling customer newsletter subscriptions with
email validation and confirmation tracking.
"""

import uuid

from django.db import models
from django.utils import timezone


class NewsletterSubscriber(models.Model):
    """
    Newsletter subscriber model with double opt-in confirmation.
    
    Tracks customer email subscriptions, confirmation status, and
    subscription dates for the Tales & Tails newsletter system.
    
    Attributes:
        email: Unique subscriber email address
        is_confirmed: Whether email confirmation is complete
        confirmation_token: UUID token for email confirmation
        subscribed_at: Initial subscription timestamp
        confirmed_at: Email confirmation timestamp
        is_active: Current subscription status
    """
    
    email = models.EmailField(
        unique=True,
        help_text="Subscriber's email address"
    )
    is_confirmed = models.BooleanField(
        default=False,
        help_text="Email confirmation status"
    )
    confirmation_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Email confirmation token"
    )
    subscribed_at = models.DateTimeField(
        default=timezone.now,
        help_text="Subscription creation date"
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Email confirmation date"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Active subscription status"
    )
    
    class Meta:
        """Model metadata and display options."""
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
    
    def __str__(self):
        """Return email address with confirmation status."""
        status = "✅ Confirmed" if self.is_confirmed else "⏳ Pending"
        return f"{self.email} - {status}"