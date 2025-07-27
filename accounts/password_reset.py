from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_password_reset_email(user):
    """Send password reset email with token"""
    # Generate token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build reset URL
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    reset_url = f"{site_url}/accounts/reset/{uid}/{token}/"
    
    context = {
        'user': user,
        'reset_url': reset_url,
    }
    
    # Create the email
    subject = 'Tales & Tails - Password Reset'
    
    # Plain text version
    text_content = f"""
Password Reset Request

Dear {user.first_name if user.first_name else 'Valued Customer'},

You recently requested to reset your password for your Tales & Tails account. Click the link below to reset it:

{reset_url}

If you did not request a password reset, please ignore this email or contact us if you have concerns.

This password reset link will expire in 24 hours.
    """
    
    # HTML version
    try:
        html_content = render_to_string('emails/password_reset.html', context)
    except:
        html_content = None
    
    # Send email
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        
        msg.send()
        return True
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False
