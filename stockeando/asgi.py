"""
ASGI config for stockeando project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockeando.settings')

application = get_asgi_application()