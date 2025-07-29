"""
Reset database migration history.

This script clears all migration history from the database by deleting all
records from the django_migrations table. This is useful when you want to
reset migrations without affecting the actual database structure.

Warning: This script should be used with caution as it removes all migration
records, which can lead to inconsistencies if the database schema doesn't
match what Django expects in a fresh migration.
"""
import os
import django


# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')
django.setup()

# Import database connection after Django is configured
from django.db import connection


def reset_migration_history():
    """
    Clear all migration records from the database.
    
    Executes a SQL command to delete all records from the django_migrations
    table and commits the changes.
    
    Returns:
        None
    """
    cursor = connection.cursor()
    cursor.execute("DELETE FROM django_migrations;")
    connection.commit()
    print("Migration history cleared successfully!")


# Execute the reset function when script is run directly
if __name__ == "__main__":
    reset_migration_history()
    