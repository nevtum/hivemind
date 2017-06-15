from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import DomainEvent, Manufacturer, Project


class DefectAPITests(APITestCase):
    def _load_fixtures(self):
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
    def setUp(self):
        self._load_fixtures()
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        user = User.objects.create_user(username, email, password)
        self.client.force_authenticate(user)
    
    def test_create_new_defect(self):
        data = { 
            'project_code': 'ABC.321',
            'release_id': 'v5.79.28.815',
            'priority': 'Low',
            'reference': 'A Title',
            'description': 'A description.',
            'comments': 'A few comments.',
        }
        response = self.client.post(reverse('defects:api:create'), data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
