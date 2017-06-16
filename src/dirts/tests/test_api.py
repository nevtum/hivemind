from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import DomainEvent, Manufacturer, Project
from .fixtures import TestFixtureMixin, RestFrameworkFakeUserLoginMixin

class DefectAPITests(TestFixtureMixin, RestFrameworkFakeUserLoginMixin, APITestCase):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        seff.assertEqual(**response.data, **data)