"""
Email testing utilities for the Django application.

This module provides view functions for testing the email configuration
and sending capabilities of the application.
"""
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings


def test_email_public(request):
    """
    Test if the email system is configured and working properly.
    
    This view attempts to send a test email and displays the results along with
    the current email configuration settings. It can be used to verify that
    the email sending functionality is working correctly in the application.
    
    Args:
        request: The HTTP request object, which may contain a GET parameter
                'email' specifying the recipient email address
                
    Returns:
        HttpResponse: HTML page showing the test results and configuration
        
    Note:
        This view displays sensitive configuration information and should
        be secured or disabled in production environments.
    """
    try:
        # Get the recipient email (use DEFAULT_FROM_EMAIL as fallback)
        default_recipient = getattr(
            settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL
        )
        recipient = request.GET.get('email', default_recipient)
        
        # Send a test email
        send_mail(
            subject='Tales & Tails - Email System Test',
            message='This is a test email from your Django application. If you '
                    'receive this, your email system is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        # Display success message with settings
        html = f"""
        <h1>Email Test Results</h1>
        <p style="color:green">✅ Test email sent successfully to {recipient}!</p>
        
        <h2>Email Configuration</h2>
        <ul>
            <li><strong>EMAIL_BACKEND:</strong> {settings.EMAIL_BACKEND}</li>
            <li><strong>EMAIL_HOST:</strong> {settings.EMAIL_HOST}</li>
            <li><strong>EMAIL_PORT:</strong> {settings.EMAIL_PORT}</li>
            <li><strong>EMAIL_USE_TLS:</strong> {settings.EMAIL_USE_TLS}</li>
            <li><strong>EMAIL_HOST_USER:</strong> {settings.EMAIL_HOST_USER}</li>
            <li><strong>DEFAULT_FROM_EMAIL:</strong> {settings.DEFAULT_FROM_EMAIL}</li>
        </ul>
        
        <p><a href="/">Return to Homepage</a></p>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        # Display error message
        html = f"""
        <h1>Email Test Failed</h1>
        <p style="color:red">❌ Error: {str(e)}</p>
        
        <h2>Email Configuration</h2>
        <ul>
            <li><strong>EMAIL_BACKEND:</strong> {settings.EMAIL_BACKEND}</li>
            <li><strong>EMAIL_HOST:</strong> {settings.EMAIL_HOST}</li>
            <li><strong>EMAIL_PORT:</strong> {settings.EMAIL_PORT}</li>
            <li><strong>EMAIL_USE_TLS:</strong> {settings.EMAIL_USE_TLS}</li>
            <li><strong>EMAIL_HOST_USER:</strong> {settings.EMAIL_HOST_USER}</li>
            <li><strong>DEFAULT_FROM_EMAIL:</strong> {settings.DEFAULT_FROM_EMAIL}</li>
        </ul>
        
        <p><a href="/">Return to Homepage</a></p>
        """
        
        return HttpResponse(html)
        