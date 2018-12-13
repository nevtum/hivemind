from defects.models import Defect
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = """fix for updating last updated dates in defects"""

    def handle(self, *args, **options):
        for defect in Defect.objects.all():
            defect.save()