from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from common.models import DomainEvent
from dirts.models import Defect, Priority, Status
from dirts.forms import CreateDirtForm

class DefectAcceptanceTests(TestCase):
    
    @staticmethod
    def _load_fixtures():
        Status.objects.create(name='Open')
        Status.objects.create(name='Closed')
        Priority.objects.create(name='High')
        Priority.objects.create(name='Medium')
        Priority.objects.create(name='Low')
        Priority.objects.create(name='Observational')
    
    def _login_fake_user(self):
        username = 'test_user'
        email = 'test@test.com'
        password = 'test_password'
        self.test_user = User.objects.create_user(username, email, password)
        login = self.client.login(username='test_user', password='test_password')
        self.assertEquals(login, True)

    @staticmethod
    def _test_form_data_with_comments():
        return {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
            'comments': 'some comments',
        }
    
    @staticmethod
    def _test_form_data_without_comments():
        return {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
        }

    def setUp(self):
        self._load_fixtures()
        self._login_fake_user()
        
    def test_should_open_correct_form_when_create_defect_url_accessed(self):
        response = self.client.get(reverse('create-dirt-url'))
        self.assertIsInstance(response.context['form'], CreateDirtForm)
    
    def test_should_pass_valid_create_defect_form_with_comments(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        self.assertEquals(form.is_valid(), True)
    
    def test_should_pass_valid_create_defect_form_without_comments(self):
        form = CreateDirtForm(data=self._test_form_data_without_comments())
        self.assertEquals(form.is_valid(), True)
    
    def test_should_create_new_defect(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        defect = form.save(commit=False)
        defect.submitter = self.test_user
        defect.raise_new()
        
        self.assertEquals(defect.project_code, 'ABC.123')
        self.assertEquals(defect.release_id, 'v1.2.3.4')
        self.assertEquals(defect.status.name, 'Open')
        self.assertEquals(defect.priority.name, 'High')
        self.assertEquals(defect.reference, 'a title')
        self.assertEquals(defect.description, 'some defect description')
        self.assertEquals(defect.comments, 'some comments')
        
    def test_should_create_dirt_opened_event(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        defect = form.save(commit=False)
        defect.submitter = self.test_user
        event = defect.raise_new()
        
        self.assertEquals(event.sequence_nr, 0)
        self.assertEquals(event.event_type, 'DIRT.OPENED')
        self.assertIsNotNone(event.blob)