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

    def test_invalid_header(self):
        data = { 'id': 123 }
        response = self.client.post(reverse('commands'), data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data.get('request-data'), data)
