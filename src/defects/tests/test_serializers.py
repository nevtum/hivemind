from api.defects.serializers import CreateDefectSerializer
from common.models import Manufacturer, Project
from defects.models import Priority
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django.utils import timezone


class SerializerTests(TransactionTestCase):
    def setUp(self):
        User.objects.create_user('test_user', 'test@email.com')
        manufacturer = Manufacturer.objects.create(
            name='Example Manufacturer',
            is_operational=True
        )
        Project.objects.create(
            code='ABC.321',
            manufacturer=manufacturer,
            description='Project 1',
            date_created=timezone.now()
        )
        Priority.objects.create(name='Low')
        
    def test_create_new_defect(self):
        data = { 
            'project_code': 'ABC.321',
            'release_id': 'v5.79.28.815',
            'priority': 'Low',
            'reference': 'A Title',
            'description': 'A description.',
            'comments': 'A few comments.',
        }
        serializer = CreateDefectSerializer(data=data)
        self.assertEquals(serializer.is_valid(), True, "{}".format(serializer.errors))
        defect = serializer.save(submitter=User.objects.get(username='test_user'))
        self.assertEqual(defect.project_code, data['project_code'])
