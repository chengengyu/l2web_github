import os
import sys

import django.core.handlers.wsgi

sys.path.append(r'M:/Users/eling/workspace/Django/l2website/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'l2website.settings'
application = django.core.handlers.wsgi.WSGIHandler()