import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ratio_Nais_Desc.settings")
application = get_wsgi_application()
app = application
