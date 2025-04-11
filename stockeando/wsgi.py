"""
WSGI config for stockeando project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockeando.settings')

application = get_wsgi_application()