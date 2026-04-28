import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn.settings')

import django
django.setup()

from django.core.management import call_command

# Ejecutar migraciones automáticamente
call_command('migrate', interactive=False)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
