"""
Django admin interface testing script.

This script tests the Django admin interface by simulating a request to the
admin index page and listing all registered models. It helps verify that the
admin configuration is working correctly without running the full server.
"""
import os
import sys
import traceback

import django


def setup_django_environment():
    """
    Set up the Django environment.
    
    Configures Django settings and initialises the Django application
    to allow for testing of Django components outside of a web server.
    
    Returns:
        None
    """
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
    django.setup()


def test_admin_index():
    """
    Test the Django admin index page.
    
    Creates a simulated request to the admin index page to verify
    that it can be rendered without errors.
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Import after Django setup to avoid AppRegistry errors
    from django.contrib.admin.sites import site
    from django.test.client import RequestFactory
    
    # Create a fake request
    factory = RequestFactory()
    request = factory.get('/admin/')
    
    # Try to get admin index
    try:
        print("Testing admin site...")
        response = site.index(request)
        print("✅ Admin index works!")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return False


def list_registered_models():
    """
    List all models registered in the Django admin.
    
    Prints a list of all models that have been registered with the
    Django admin site, which helps verify admin configurations.
    
    Returns:
        None
    """
    # Import after Django setup
    from django.contrib.admin.sites import site
    
    print("\nRegistered admin models:")
    for model, admin_obj in site._registry.items():
        print(f" - {model.__name__}")


def main():
    """
    Execute the admin testing script.
    
    Runs the setup and testing functions in sequence to verify
    the Django admin functionality.
    
    Returns:
        None
    """
    setup_django_environment()
    test_admin_index()
    list_registered_models()


# Run the script
if __name__ == "__main__":
    main()