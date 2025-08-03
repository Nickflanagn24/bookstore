from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import NewsletterSubscriber
import logging

logger = logging.getLogger(__name__)

def subscribe_newsletter(request):
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
                messages.success(request, f'🎉 Confirmation email sent to {email}!')
            except Exception as e:
                messages.error(request, 'Error sending confirmation email.')
        else:
            if subscriber.is_confirmed:
                messages.info(request, 'You are already subscribed! 📬')
            else:
                try:
                    send_confirmation_email(subscriber, request)
                    messages.info(request, f'📧 New confirmation email sent to {email}.')
                except Exception as e:
                    messages.error(request, 'Error sending confirmation email.')
    
    return redirect('home')

def send_confirmation_email(subscriber, request):
    confirmation_url = request.build_absolute_uri(
        reverse('newsletter:confirm', kwargs={'token': subscriber.confirmation_token})
    )
    
    context = {
        'confirmation_url': confirmation_url,
        'subscriber': subscriber,
    }
    
    html_message = render_to_string('emails/newsletter_confirmation.html', context)
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
    try:
        subscriber = get_object_or_404(NewsletterSubscriber, confirmation_token=token)
        
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
        messages.error(request, 'Error confirming subscription.')
    
    return redirect('home')

def send_welcome_email(subscriber):
    context = {'subscriber': subscriber}
    
    html_message = render_to_string('emails/newsletter_welcome.html', context)
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
    try:
        subscriber = get_object_or_404(NewsletterSubscriber, confirmation_token=token)
        
        if request.method == 'POST':
            subscriber.is_active = False
            subscriber.save()
            messages.success(request, '😢 Unsubscribed successfully.')
            return redirect('home')
        
        return render(request, 'newsletter/unsubscribe.html', {'subscriber': subscriber})
    
    except Exception as e:
        messages.error(request, 'Error processing request.')
        return redirect('home')
