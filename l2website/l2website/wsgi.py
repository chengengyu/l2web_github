"""
WSGI config for l2website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys
sys.path.append(r'c:/l2website/')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "l2website.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()