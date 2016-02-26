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
    
    def _create_fake_user(self):
        self.username = 'test_user'
        self.email = 'test@test.com'
        self.password = 'test_password'        
        self.test_user = User.objects.create_user(
            self.username, self.email, self.password)
    
    def setUp(self):
        self._load_fixtures()
        self._create_fake_user()
        
    def test_should_create_new_defect(self):
        kwargs = {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
            'comments': 'some comments',
        }
        form = CreateDirtForm(kwargs)
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
        kwargs = {
            'project_code': 'ABC.123',
            'release_id': 'v1.2.3.4',
            'priority': Priority.objects.get(name='High').id,
            'reference': 'a title',
            'description': 'some defect description',
            'comments': 'some comments',
        }
        form = CreateDirtForm(kwargs)
        defect = form.save(commit=False)
        defect.submitter = self.test_user
        defect.raise_new()
        
        events = DomainEvent.objects.filter(aggregate_type='DEFECT', aggregate_id=defect.id)
        event = events.last()
        self.assertEquals(len(events), 1)
        self.assertEquals(event.sequence_nr, 0)
        self.assertEquals(event.event_type, 'DIRT.OPENED')