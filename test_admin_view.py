#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

from django.test import Client
client = Client()
response = client.get('/admin/', follow=True)
print(f"Status code: {response.status_code}")
print(f"Template used: {[t.name for t in response.templates]}")
print(f"Content: {response.content[:200]}...")
