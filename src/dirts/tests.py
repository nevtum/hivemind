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
    
    def _assert_empty_field_fail_form(self, field_name, value):
        kwargs = self._test_form_data_with_comments()
        kwargs[field_name] = value
        form = CreateDirtForm(data=kwargs)
        self.assertEquals(form.is_valid(), False)
        
    def test_should_fail_valid_create_defect_form_with_empty_project_code(self):
        self._assert_empty_field_fail_form('project_code', '')
        
    def test_should_fail_valid_create_defect_form_with_empty_release_id(self):
        self._assert_empty_field_fail_form('release_id', '')
        
    def test_should_fail_valid_create_defect_form_with_empty_priority(self):
        self._assert_empty_field_fail_form('priority', None)
    
    def test_should_fail_valid_create_defect_form_with_empty_reference(self):
        self._assert_empty_field_fail_form('reference', '')
    
    def test_should_fail_valid_create_defect_form_with_empty_description(self):
        self._assert_empty_field_fail_form('description', '')
    
    def test_should_pass_valid_create_defect_form_with_comments(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        self.assertEquals(form.is_valid(), True)
    
    def test_should_pass_valid_create_defect_form_without_comments(self):
        form = CreateDirtForm(data=self._test_form_data_without_comments())
        self.assertEquals(form.is_valid(), True)
    
    def test_should_create_new_defect(self):
        response = self.client.post(
            reverse('create-dirt-url'),
            data=self._test_form_data_with_comments(),
            follow=True)

        result = response.context['dirt']
        
        self.assertEquals(result.project_code, 'ABC.123')
        self.assertEquals(result.release_id, 'v1.2.3.4')
        self.assertEquals(result.status, 'Open')
        self.assertEquals(result.priority, 'High')
        self.assertEquals(result.reference, 'a title')
        self.assertEquals(result.description, 'some defect description')
        self.assertEquals(result.comments, 'some comments')
        
    
    def test_should_update_existing_defect(self):
        data = self._test_form_data_with_comments()
        
        response = self.client.post(
            reverse('create-dirt-url'),
            data=data,
            follow=True)
        
        data['project_code'] = 'ABC.321'
        data['release_id'] = 'v4.3.2.1'
        data['priority'] = Priority.objects.get(name='Observational').id
        data['reference'] = 'changed title'
        data['description'] = 'modified description'
        data['comments'] = 'updated comments'
        
        dirt_id = response.context['dirt'].id
        
        response = self.client.post(
            reverse('dirt-amend-url', kwargs={'dirt_id': dirt_id}),
            data=data,
            follow=True)

        result = response.context['dirt']
        
        self.assertEquals(result.project_code, 'ABC.321')
        self.assertEquals(result.release_id, 'v4.3.2.1')
        self.assertEquals(result.status, 'Open')
        self.assertEquals(result.priority, 'Observational')
        self.assertEquals(result.reference, 'changed title')
        self.assertEquals(result.description, 'modified description')
        self.assertEquals(result.comments, 'updated comments')
        
    def test_should_create_dirt_opened_event(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        defect = form.save(commit=False)
        defect.submitter = self.test_user
        event = defect.raise_new()
        
        self.assertEquals(event.sequence_nr, 0)
        self.assertEquals(event.event_type, 'DIRT.OPENED')
        self.assertIsNotNone(event.blob)