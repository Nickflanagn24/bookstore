import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

from django.db import connection

# Clear migration history
cursor = connection.cursor()
cursor.execute("DELETE FROM django_migrations;")
connection.commit()
print("Migration history cleared successfully!")
