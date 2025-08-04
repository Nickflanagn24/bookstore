"""
Newsletter subscription views for Tales & Tails bookstore.

Handles newsletter signup, email confirmation, welcome emails,
and unsubscription functionality with double opt-in system.
"""

import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from .models import NewsletterSubscriber


logger = logging.getLogger(__name__)


def subscribe_newsletter(request):
    """
    Handle newsletter subscription requests.
    
    Processes POST requests for newsletter signup, creates or retrieves
    subscriber records, and sends confirmation emails.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('home')
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_confirmed': False}
        )
        
        if created:
            try:
                send_confirmation_email(subscriber, request)
                messages.success(
                    request, f'🎉 Confirmation email sent to {email}!'
                )
            except Exception as e:
                logger.error(f'Error sending confirmation email: {e}')
                messages.error(request, 'Error sending confirmation email.')
        else:
            if subscriber.is_confirmed:
                messages.info(request, 'You are already subscribed! 📬')
            else:
                try:
                    send_confirmation_email(subscriber, request)
                    messages.info(
                        request, f'📧 New confirmation email sent to {email}.'
                    )
                except Exception as e:
                    logger.error(f'Error sending confirmation email: {e}')
                    messages.error(request, 'Error sending confirmation email.')
    
    return redirect('home')


def send_confirmation_email(subscriber, request):
    """
    Send confirmation email to new newsletter subscriber.
    
    Generates confirmation URL and sends HTML/plain text email
    with subscription confirmation link.
    """
    confirmation_url = request.build_absolute_uri(
        reverse('newsletter:confirm', kwargs={
            'token': subscriber.confirmation_token
        })
    )
    
    context = {
        'confirmation_url': confirmation_url,
        'subscriber': subscriber,
    }
    
    html_message = render_to_string(
        'emails/newsletter_confirmation.html', context
    )
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='🐕 Confirm your Tales & Tails newsletter subscription',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email],
        html_message=html_message,
        fail_silently=False,
    )


def confirm_subscription(request, token):
    """
    Confirm newsletter subscription via email token.
    
    Validates confirmation token, updates subscriber status,
    and sends welcome email upon successful confirmation.
    """
    try:
        subscriber = get_object_or_404(
            NewsletterSubscriber, confirmation_token=token
        )
        
        if not subscriber.is_confirmed:
            subscriber.is_confirmed = True
            subscriber.confirmed_at = timezone.now()
            subscriber.save()
            
            # Send welcome email
            send_welcome_email(subscriber)
            messages.success(request, '🎉 Welcome to Tales & Tails newsletter!')
        else:
            messages.info(request, '✅ Already confirmed!')
    
    except Exception as e:
        logger.error(f'Error confirming subscription: {e}')
        messages.error(request, 'Error confirming subscription.')
    
    return redirect('home')


def send_welcome_email(subscriber):
    """
    Send welcome email to confirmed newsletter subscriber.
    
    Sends branded welcome message with HTML/plain text versions
    to newly confirmed subscribers.
    """
    context = {'subscriber': subscriber}
    
    html_message = render_to_string(
        'emails/newsletter_welcome.html', context
    )
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject='🐾 Welcome to Tales & Tails Newsletter!',
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email],
        html_message=html_message,
        fail_silently=False,
    )


def unsubscribe(request, token):
    """
    Handle newsletter unsubscription requests.
    
    Displays confirmation page for GET requests and processes
    unsubscription for POST requests using email token.
    """
    try:
        subscriber = get_object_or_404(
            NewsletterSubscriber, confirmation_token=token
        )
        
        if request.method == 'POST':
            subscriber.is_active = False
            subscriber.save()
            messages.success(request, '😢 Unsubscribed successfully.')
            return redirect('home')
        
        return render(request, 'newsletter/unsubscribe.html', {
            'subscriber': subscriber
        })
    
    except Exception as e:
        logger.error(f'Error processing unsubscribe request: {e}')
        messages.error(request, 'Error processing request.')
        return redirect('home')