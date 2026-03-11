"""Import Django models for use in FastAPI.

This module imports Django models so they can be used
in FastAPI endpoints and authentication.
"""
import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idmitra_django.settings")
django.setup()

# Import Django models
from core.models import APIKey, User, Meeting

__all__ = ["APIKey", "User", "Meeting"]

