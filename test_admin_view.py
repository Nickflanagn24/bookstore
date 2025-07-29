#!/usr/bin/env python
"""
Django admin interface testing script.

This script tests the Django admin interface by making an HTTP request to the
admin index page and displaying information about the response. It helps verify
that the admin site is accessible and functioning correctly without manually
opening a browser.
"""
import os
import django


def setup_django_environment():
    """
    Set up the Django environment.
    
    Configures Django settings and initialises the Django application
    to allow for testing of Django components outside of a web server.
    
    Returns:
        None
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
    django.setup()


def test_admin_access():
    """
    Test access to the Django admin site.
    
    Makes an HTTP request to the admin index page and prints information
    about the response including status code, templates used, and the
    beginning of the content.
    
    Returns:
        None
    """
    from django.test import Client
    
    # Create a test client
    client = Client()
    
    # Make a GET request to the admin site
    response = client.get('/admin/', follow=True)
    
    # Print response information
    print(f"Status code: {response.status_code}")
    print(f"Template used: {[t.name for t in response.templates]}")
    print(f"Content: {response.content[:200]}...")


def main():
    """
    Execute the admin testing script.
    
    Runs the setup and testing functions in sequence to verify
    the Django admin functionality.
    
    Returns:
        None
    """
    setup_django_environment()
    test_admin_access()


# Run the script
if __name__ == "__main__":
    main()
    