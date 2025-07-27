import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

# Import necessary modules
from django.contrib.admin.sites import site
from django.urls import reverse
from django.test.client import RequestFactory

# Create a fake request
factory = RequestFactory()
request = factory.get('/admin/')

# Try to get admin index
try:
    print("Testing admin site...")
    response = site.index(request)
    print("✅ Admin index works!")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

# Check registered models
print("\nRegistered admin models:")
for model, admin_obj in site._registry.items():
    print(f" - {model.__name__}")

