import os, sys
from django.core.wsgi import get_wsgi_application

proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(proj_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "echelon.settings.prod")
application = get_wsgi_application()

from dirts.models import Defect

if __name__ == '__main__':
    for defect in Defect.objects.all():
        defect.save()