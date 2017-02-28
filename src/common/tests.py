from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class CommandHandlerTests(APITestCase):
    def setUp(self):
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        user = User.objects.create_user(username, email, password)
        self.client.force_authenticate(user)

    def test_missing_header(self):
        data = { 'id': 123 }
        response = self.client.post(reverse('commands'), data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = 'Please provide a COMMAND type in request header'
        self.assertEquals(response.data.get('detail'), error_msg)

    def test_invalid_header(self):
        data = { 'id': 123 }
        response = self.client.post(reverse('commands'), data, format='json', HTTP_COMMAND='unknown-command')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_msg = 'Could not find a handler for the given COMMAND type'
        self.assertEquals(response.data.get('detail'), error_msg)