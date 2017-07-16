from django.contrib.auth.models import User
from django.utils import timezone

from common.models import DomainEvent, Manufacturer, Project

class RestFrameworkFakeUserLoginMixin(object):
    def login_fake_user(self):
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        user = User.objects.create_user(username, email, password)
        self.client.force_login(user)

class DjangoFakeUserLoginMixin(object):
    def login_fake_user(self):
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        self.test_user = User.objects.create_user(username, email, password)
        login = self.client.login(username='test_user', password='test_password')
        self.assertEqual(login, True)

class TestFixtureMixin(object):
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

    def setUp(self):
        self._load_fixtures()
        self.login_fake_user()
