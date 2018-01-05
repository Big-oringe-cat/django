import os
import sys
import django.core.handlers.wsgi

proj = os.path.dirname(__file__)
projs = os.path.dirname(proj)
if projs not in sys.path:
    sys.path.append(proj)
    sys.path.append(projs)

os.environ['DJANGO_SETTINGS_MODULE'] = 'YWmanager.settings'
application = django.core.handlers.wsgi.WSGIHandler()


"""
WSGI config for a project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see#https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a.settings")

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
