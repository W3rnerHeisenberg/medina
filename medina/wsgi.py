"""
WSGI config for medina project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

# ESTO ES LO NUEVO: Forzamos a Python a mirar en la carpeta raíz
# donde vive tu app 'crypto'
sys.path.append('/home/rut/medina')
sys.path.append('/home/rut/medina/medina')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medina.settings')

application = get_wsgi_application()