#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the entry point for Django's management commands such as
runserver, makemigrations, migrate, etc. It sets up the environment and
delegates to Django's command system.
"""
import os
import sys


def main():
    """
    Run administrative tasks.
    
    Sets up the Django environment, processes command-line arguments,
    and executes the appropriate Django management command.
    
    Raises:
        ImportError: If Django cannot be imported, suggesting issues
                     with installation or the Python environment
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()