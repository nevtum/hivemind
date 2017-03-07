from common.models import DomainEvent, Manufacturer, Project
from .forms import CreateDirtForm, ImportDirtForm
from .models import Defect, Priority, Status
from .serializers import ImportDefectSerializer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

class DefectAcceptanceTests(TestCase):
    
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
        self.assertEqual(form.is_valid(), False)
        
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
        self.assertEqual(form.is_valid(), True)
    
    def test_should_pass_valid_create_defect_form_without_comments(self):
        form = CreateDirtForm(data=self._test_form_data_without_comments())
        self.assertEqual(form.is_valid(), True)
    
    def test_should_create_new_defect(self):
        data = self._test_form_data_with_comments()
        create_defect_page = CreateDefectPage(self.client)
        defect_page = create_defect_page.raise_new_defect(**data)
        result = defect_page.context
        
        self.assertEqual(result.project_code, 'ABC.123')
        self.assertEqual(result.release_id, 'v1.2.3.4')
        self.assertEqual(result.status, 'Open')
        self.assertEqual(result.priority, 'High')
        self.assertEqual(result.reference, 'a title')
        self.assertEqual(result.description, 'some defect description')
        self.assertEqual(result.comments, 'some comments')
        
    def test_should_update_existing_defect(self):
        data = self._test_form_data_with_comments()
        
        create_defect_page = CreateDefectPage(self.client)
        defect_page = create_defect_page.raise_new_defect(**data)
        
        data['project_code'] = 'ABC.321'
        data['release_id'] = 'v4.3.2.1'
        data['priority'] = Priority.objects.get(name='Observational').id
        data['reference'] = 'changed title'
        data['description'] = 'modified description'
        data['comments'] = 'updated comments'
        
        defect_page.amend_defect(**data)
        result = defect_page.context
        
        self.assertEqual(result.project_code, 'ABC.321')
        self.assertEqual(result.release_id, 'v4.3.2.1')
        self.assertEqual(result.status, 'Open')
        self.assertEqual(result.priority, 'Observational')
        self.assertEqual(result.reference, 'changed title')
        self.assertEqual(result.description, 'modified description')
        self.assertEqual(result.comments, 'updated comments')
        
        self.assertEqual(len(result.change_history), 2)
        self.assertEqual(result.change_history[-1].submitter, 'test_user')
    
    def test_should_close_existing_defect(self):
        data = self._test_form_data_with_comments()   
        create_defect_page = CreateDefectPage(self.client)
        defect_page = create_defect_page.raise_new_defect(**data)
        defect_page.close_defect('v1.2.3.5')
        result = defect_page.context
        
        self.assertEqual(result.status, 'Closed')
        self.assertEqual(result.release_id, 'v1.2.3.5')
    
    def test_should_reopen_a_closed_defect(self):
        data = self._test_form_data_with_comments()
        create_defect_page = CreateDefectPage(self.client)
        defect_page = create_defect_page.raise_new_defect(**data)
        defect_page.close_defect('v1.2.3.5')
        defect_page.reopen_defect('v1.2.4.2', 'issue regressed')
        result = defect_page.context
        
        self.assertEqual(result.status, 'Open')
        self.assertEqual(result.release_id, 'v1.2.4.2')
        
        # test put here to prevent a bug from the past from regressing
        expected_priority = Priority.objects.get(pk=data['priority']).name
        self.assertEqual(result.priority, expected_priority)
        
    def test_should_create_dirt_opened_event(self):
        form = CreateDirtForm(data=self._test_form_data_with_comments())
        defect = form.save(commit=False)
        defect.submitter = self.test_user
        event = defect.raise_new()
        
        self.assertEqual(event['sequence_nr'], 0)
        self.assertEqual(event['event_type'], 'DIRT.OPENED')
        self.assertIsNotNone(event['payload'])
    
    def test_should_import_dirt_date_provided(self):
        data = self._test_form_data_with_comments()
        
        status = Status.objects.get(name='Open')
        data['date_created'] = timezone.datetime(2017, 3, 7)
        data['submitter'] = self.test_user.id
        data['status'] = status.id

        form = ImportDirtForm(data=data)
        self.assertEqual(form.is_valid(), True)
        tzdate = form.cleaned_data['date_created']
        defect = form.save(commit=False)
        
        self.assertEqual(defect.submitter, self.test_user)
        self.assertEqual(defect.release_id, data['release_id'])
        self.assertEqual(defect.status, status)
        self.assertEqual(defect.date_created, tzdate)
    
    def test_should_deserialize_json_defect(self):
        data = {
            'project_code': 'ABC.321',
            'date_created': '2017-03-06T00:00:00+11:00',
            'priority': 'High',
            'status': 'Open',
            'submitter': self.test_user.username,
            'release_id': 'v1.23.456',
            'reference': 'Failed to get into particular state',
            'description': 'Simple description',
            'comments': ''
        }
        serializer = ImportDefectSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True, serializer.errors)
        defect = serializer.save()
        self.assertEqual(isinstance(defect, Defect), True)
        self.assertEqual(defect.project, Project.objects.get(code='ABC.321'))
        self.assertEqual(defect.submitter, self.test_user)
        self.assertEqual(defect.priority, Priority.objects.get(name='High'))
        self.assertEqual(defect.status, Status.objects.get(name='Open'))


class CreateDefectPage:
    """Helper class abstracting away web call details
    and focusing on the intent of the tests"""
    def __init__(self, client):
        self.client = client
    
    def raise_new_defect(self, **post_data):
        response = self.client.post(
            reverse('create-dirt-url'),
            data=post_data,
            follow=True
        )
        assert(response.status_code == 200)
        return DefectPage(self.client, response.context['model'].id)

class DefectPage:
    """Helper class abstracting away web call details
    and focusing on the intent of the tests"""
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.response = self.client.get(
            reverse('dirt-detail-url', kwargs={'pk': self.id})
        )
    
    def close_defect(self, release_id, reason=None):
        post_data = {
            'release_id': release_id,
            'reason': reason
        }
        self.response = self.client.post(
            reverse('dirt-close-url', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
        assert(self.response.status_code == 200)
        
    def reopen_defect(self, release_id, reason):
        post_data = {
            'release_id': release_id,
            'reason': reason
        }
        self.response = self.client.post(
            reverse('dirt-reopen-url', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
        assert(self.response.status_code == 200)
    
    def amend_defect(self, **post_data):
        self.response = self.client.post(
            reverse('dirt-amend-url', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
    
    @property
    def context(self):
        defect = self.response.context['model']
        return defect.as_domainmodel()
