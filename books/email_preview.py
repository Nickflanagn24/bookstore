from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import datetime

def preview_email_template(request, template_name):
    """Preview email templates with sample data (only in DEBUG mode)"""
    # Only allow in DEBUG mode for security
    if not settings.DEBUG:
        return HttpResponse("Email preview only available in DEBUG mode.", status=403)
    
    context = {}
    
    # Sample data based on template
    if template_name == 'order_confirmation':
        # Create dummy order data
        class DummyAddress:
            name = "John Doe"
            address_line1 = "123 Book Lane"
            address_line2 = "Apt 4B"
            city = "London"
            postal_code = "W1A 1AA"
            country = "United Kingdom"
        
        class DummyBook:
            title = "The Dog Whisperer"
        
        class DummyItem:
            book = DummyBook()
            quantity = 2
            price = "24.99"
        
        class DummyUser:
            first_name = "John"
            email = "john@example.com"
        
        class DummyItems:
            @staticmethod
            def all():
                return [DummyItem(), DummyItem()]
        
        class DummyOrder:
            id = "ORD-12345"
            created_at = datetime.datetime.now()
            payment_method = "Credit Card"
            shipping_cost = "3.99"
            subtotal = "49.98"
            total = "53.97"
            user = DummyUser()
            shipping_address = DummyAddress()
            items = DummyItems()
        
        order = DummyOrder()
        
        context = {
            'order': order,
            'order_url': 'https://example.com/order/12345',
            'contact_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'contact@example.com'),
        }
    
    elif template_name == 'shipping_notification':
        # Create dummy order data for shipping
        class DummyAddress:
            name = "John Doe"
            address_line1 = "123 Book Lane"
            address_line2 = "Apt 4B"
            city = "London"
            postal_code = "W1A 1AA"
            country = "United Kingdom"
        
        class DummyBook:
            title = "The Dog Whisperer"
        
        class DummyItem:
            book = DummyBook()
            quantity = 2
        
        class DummyUser:
            first_name = "John"
            email = "john@example.com"
        
        class DummyItems:
            @staticmethod
            def all():
                return [DummyItem(), DummyItem()]
        
        class DummyOrder:
            id = "ORD-12345"
            shipping_date = datetime.datetime.now()
            estimated_delivery = datetime.datetime.now() + datetime.timedelta(days=3)
            tracking_number = "GB123456789GB"
            user = DummyUser()
            shipping_address = DummyAddress()
            items = DummyItems()
        
        order = DummyOrder()
        
        context = {
            'order': order,
            'order_url': 'https://example.com/order/12345',
            'tracking_url': 'https://www.royalmail.com/track-your-item',
            'contact_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'contact@example.com'),
        }
    
    elif template_name == 'password_reset':
        class DummyUser:
            first_name = "John"
            email = "john@example.com"
        
        context = {
            'user': DummyUser(),
            'reset_url': 'https://example.com/reset/token123/',
        }
    
    try:
        html_content = render_to_string(f'emails/{template_name}.html', context)
        return HttpResponse(html_content)
    except Exception as e:
        return HttpResponse(f"Error loading template: {str(e)}")
