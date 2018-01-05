import os
import sys
import django.core.handlers.wsgi

proj = os.path.dirname(__file__)
projs = os.path.dirname(proj)
if projs not in sys.path:
    sys.path.append(proj)
    sys.path.append(projs)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Monitor_v3.settings'
application = django.core.handlers.wsgi.WSGIHandler()

