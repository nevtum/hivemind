from django.test import TestCase
from common.models import DomainEvent, Manufacturer, Project
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Defect, Priority, Status

from ..imports.serializers import ImportDefectSerializer

class DefectImportTests(TestCase):
    @staticmethod
    def _load_fixtures():
        manufacturer = Manufacturer.objects.create(
            name='Example Manufacturer',
            is_operational=True
        )
        Project.objects.create(
            code='ABC.123',
            manufacturer=manufacturer,
            description='Project 1',
            date_created=timezone.now()
        )
        Project.objects.create(
            code='ABC.321',
            manufacturer=manufacturer,
            description='Project 2',
            date_created=timezone.now()
        )
    
    def _login_fake_user(self):
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        self.test_user = User.objects.create_user(username, email, password)
        login = self.client.login(username='test_user', password='test_password')
        self.assertEqual(login, True)

    def setUp(self):
        self._load_fixtures()
        self._login_fake_user()

    @staticmethod
    def _test_serializer_data_without_comments():
        return {
            'project_code': 'ABC.321',
            'date_created': '2017-03-06T00:00:00+11:00',
            'priority': 'High',
            'status': 'Open',
            'submitter': 'test_user',
            'release_id': 'v1.23.456',
            'reference': 'Failed to get into particular state',
            'description': 'Simple description',
            'comments': ''
        }

    def test_should_deserialize_json_defect(self):
        data = self._test_serializer_data_without_comments()
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True, serializer.errors)
        defect = serializer.save()
        self.assertEqual(isinstance(defect, Defect), True)
        self.assertEqual(defect.project, Project.objects.get(code='ABC.321'))
        self.assertEqual(defect.submitter, self.test_user)
        self.assertEqual(defect.priority, Priority.objects.get(name='High'))
        self.assertEqual(defect.status, Status.objects.get(name='Open'))
    
    def test_should_deserialize_json_defect_close_date_provided(self):
        data = self._test_serializer_data_without_comments()
        data['date_changed'] = '2017-03-06T00:00:00+11:00'
        data['status'] = 'Closed'
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True, serializer.errors)
        defect = serializer.save()
        self.assertEqual(defect.status.name, data['status'])
        self.assertEqual(defect.date_created.isoformat(), data['date_created'])
        self.assertEqual(defect.date_changed.isoformat(), data['date_changed'])
    
    def test_should_accept_different_date_format(self):
        data = self._test_serializer_data_without_comments()
        data['date_created'] = '06/03/2017'
        data['date_changed'] = '06/03/17'
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True, serializer.errors)
    
    def test_should_fail_validation_deserialize_defect_date_changed_lt_date_created(self):
        data = self._test_serializer_data_without_comments()
        data['date_created'] = '2017-03-06T00:00:00+11:00'
        data['date_changed'] = '2017-03-05T00:00:00+11:00'
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
    
    def test_should_fail_validation_defect_closed_no_date_changed_provided(self):
        data = self._test_serializer_data_without_comments()
        data['status'] = 'Closed'
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False, serializer.errors)