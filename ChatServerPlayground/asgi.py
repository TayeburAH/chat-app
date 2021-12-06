import os
import django

# from django.core.asgi import get_asgi_application
from channels.routing import get_default_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatServerPlayground.settings')
django.setup()
application = get_default_application()

# Now it will work as asgi and wsgi







