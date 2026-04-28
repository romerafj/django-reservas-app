import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cn.settings')

import django
django.setup()

from django.core.management import call_command
call_command('migrate', interactive=False)

from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
