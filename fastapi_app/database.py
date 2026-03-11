"""Database utilities for FastAPI.

FastAPI uses Django ORM directly through Django models.
No SQLAlchemy needed - everything managed through Django.
"""
import os
import django

# Setup Django ORM
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "idmitra_django.settings")
django.setup()

# Now Django is ready to use

