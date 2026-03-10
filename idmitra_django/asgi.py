"""
ASGI config for idmitra_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from pathlib import Path

from django.core.asgi import get_asgi_application
from starlette.routing import Mount, Router
from starlette.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'idmitra_django.settings')

# Get Django ASGI application
django_asgi_app = get_asgi_application()

# Import FastAPI app
from fastapi_app.main import app as fastapi_app

# Define base directory for static files
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_DIR = BASE_DIR / 'static'

# Create static files app (serves collected static files)
static_app = StaticFiles(directory=str(STATIC_ROOT), check_dir=False)

# Create router with mounts
routes = [
    Mount("/static", app=static_app, name="static"),
    Mount("/api", app=fastapi_app),
    Mount("", app=django_asgi_app),
]

# Create main Starlette Router application
application = Router(routes)
