from common.models import DomainEvent, Manufacturer, Project
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from ..forms import CreateDirtForm
from ..models import Defect, Priority, Status
from ..constants import RESOLVED


class TestFixtureMixin:  
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

class DefectCommentAcceptanceTests(TestFixtureMixin, TestCase):
    def test_comment_added_to_defect(self):
        kwargs = {
            'project_code': Project.objects.get(code='ABC.123'),
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High'),
            'submitter': User.objects.get(username='test_user'),
            'reference': 'a title',
            'description': 'some defect description',
            'comments': 'some comments',
        }
        defect = Defect.objects.create(**kwargs)
        response = self.client.get(
            reverse('defects:defect-comments:list', kwargs={'pk': defect.id}),
        )
        self.assertEqual(response.status_code, 200)
        post_data = {
            'defect': defect.id,
            'content': 'My content'
        }
        response = self.client.post(
            reverse('defects:defect-comments:add', kwargs={'pk': defect.id}),
            data=post_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        comment_count = len(comments)
        self.assertEqual(comment_count, 1)
        self.assertEqual(comments[0].content, 'My content')
        self.assertEqual(comments[0].defect.id, defect.id)

    def test_comment_edited(self):
        pass

    def test_comment_deleted(self):
        pass
        

class DefectAcceptanceTests(TestFixtureMixin, TestCase):
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
    
    def test_should_open_correct_form_when_create_defect_url_accessed(self):
        response = self.client.get(reverse('defects:create'))
        self.assertIsInstance(response.context['form'], CreateDirtForm)

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

class CreateDefectPage:
    """Helper class abstracting away web call details
    and focusing on the intent of the tests"""
    def __init__(self, client):
        self.client = client
    
    def raise_new_defect(self, **post_data):
        response = self.client.post(
            reverse('defects:create'),
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
            reverse('defects:detail', kwargs={'pk': self.id})
        )
    
    def close_defect(self, release_id, reason=RESOLVED):
        post_data = {
            'release_id': release_id,
            'reason': reason
        }
        self.response = self.client.post(
            reverse('defects:close', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
        assert(self.response.redirect_chain != [])
        assert(self.response.status_code == 200)
        
    def reopen_defect(self, release_id, reason):
        post_data = {
            'release_id': release_id,
            'reason': reason
        }
        self.response = self.client.post(
            reverse('defects:reopen', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
        assert(self.response.redirect_chain != [])
        assert(self.response.status_code == 200)
    
    def amend_defect(self, **post_data):
        self.response = self.client.post(
            reverse('defects:amend', kwargs={'pk': self.id}),
            data=post_data,
            follow=True
        )
        assert(self.response.redirect_chain != [])
        assert(self.response.status_code == 200)
    
    @property
    def context(self):
        defect = self.response.context['model']
        return defect.as_domainmodel()
