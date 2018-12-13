from django.test import TransactionTestCase
from django.contrib.auth.models import User
from datetime import datetime
from ..constants import DEFECT_OPENED, DEFECT_CLOSED, DEFECT_IMPORTED, DEFECT_AMENDED, DEFECT_LOCKED
from ..domain.models import DefectViewModel as DefectModel

def get_user(username):
    return User.objects.get(username=username)

def create_new_defect():
    return {
        'sequence_nr': 0,
        'aggregate_id': 1,
        'aggregate_type': 'DEFECT',
        'event_type': DEFECT_OPENED,
        'timestamp': datetime(2014, 3, 10),
        'owner': 'test_user', # must be a user instance
        'payload': {
            'project_code': 'TEST.123',
            'release_id': 'v1.23.45',
            'priority': 'Low',
            'reference': 'My Title',
            'description': 'My Description',
            'comments': ''
        }
    }

def create_example_close_event(sequence_nr):
    return {
        'sequence_nr': sequence_nr,
        'aggregate_id': 1,
        'aggregate_type': 'DEFECT',
        'event_type': DEFECT_CLOSED,
        'timestamp': datetime(2014, 3, 12),
        'owner': 'test_user', # must be a user instance
        'payload': {
            "release_id": "v5.13.2.0",
            "reason": "Resolved."
        }
    }

def create_example_amendment():
    return {
        'project_code': 'TEST.7436',
        'release_id': 'v2.25.86',
        'priority': 'Medium',
        'status': 'Open',
        'reference': 'My Amended Title',
        'description': 'My Description',
        'comments': 'Some added comments'
    }

def import_new_defect():
    data = create_new_defect()
    data['payload'] = {
        'project_code': 'TEST.432',
        'release_id': 'v1.83.45',
        'priority': 'High',
        'status': 'Open',
        'reference': 'My Title2',
        'description': 'My Description2',
        'comments': 'With comments'
    }
    data['event_type'] = DEFECT_IMPORTED
    return data

class DefectObsoleteTests(TransactionTestCase):
    def setUp(self):
        User.objects.create_user('user2')
        User.objects.create_user('test_user')

    def test_make_obsolete_event(self):
        model = DefectModel([import_new_defect()])
        model.close(get_user('user2'), 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        event = model.make_obsolete(get_user('user2'), 'No longer applicable', datetime(2017, 5, 22, 9, 45))
        self.assertEqual(event['event_type'], DEFECT_LOCKED)
        self.assertEqual(event['payload']['reason'], 'No longer applicable')
    
    def test_lock_other_operations_when_made_obsolete(self):
        model = DefectModel([import_new_defect()])
        model.close(get_user('user2'), 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        model.make_obsolete(get_user('user2'), 'No longer applicable', datetime(2017, 5, 22, 9, 46))
        self.assertEqual(model.is_locked, True)
        self.assertEqual(model.is_active, False)
        self.assertRaises(Exception, model.reopen, get_user('user2'), 'v2.3.01', 'Bug regressed', datetime(2017, 5, 22, 9, 47))
        self.assertRaises(Exception, model.amend, get_user('user2'), datetime(2017, 5, 22, 9, 47), **create_example_amendment())
        self.assertRaises(Exception, model.close, get_user('user2'), 'v2.1.22', '', datetime(2017, 5, 22, 9, 47))        

    def test_make_obsolete_fail_if_not_closed(self):
        model = DefectModel([create_new_defect()])
        self.assertRaises(Exception, model.make_obsolete, get_user('user2'), 'No longer applicable', datetime(2017, 5, 22, 9, 46))
        self.assertEqual(model.is_locked, False)

class DefectAggregateTests(TransactionTestCase):
    def setUp(self):
        User.objects.create_user('user2')
        User.objects.create_user('test_user')

    def test_open(self):
        model = DefectModel([create_new_defect()])
        self.assertEqual(model.id, 1)
        self.assertEqual(model.release_id, 'v1.23.45')
        self.assertEqual(model.priority, 'Low')
        self.assertEqual(model.reference, 'My Title')
        self.assertEqual(model.description, 'My Description')
        self.assertEqual(model.comments, '')
        self.assertEqual(model.submitter, 'test_user')
        self.assertEqual(model.status, 'Open')
        self.assertEqual(model.date_created, datetime(2014, 3, 10))
        self.assertEqual(model.date_changed, datetime(2014, 3, 10))
    
    def test_open_invalid_input_event_datetime_format(self):
        data = create_new_defect()
        data['timestamp'] = '10/03/2017'
        self.assertRaises(AssertionError, DefectModel, [data])
    
    def test_import(self):
        model = DefectModel([import_new_defect()])
        self.assertEqual(model.id, 1)
        self.assertEqual(model.release_id, 'v1.83.45')
        self.assertEqual(model.priority, 'High')
        self.assertEqual(model.reference, 'My Title2')
        self.assertEqual(model.description, 'My Description2')
        self.assertEqual(model.submitter, 'test_user')
        self.assertEqual(model.status, 'Open')
        self.assertEqual(model.date_created, datetime(2014, 3, 10))
        self.assertEqual(model.date_changed, datetime(2014, 3, 10))
    
    def test_amend(self):
        model = DefectModel([import_new_defect()])
        amendment_kwargs = create_example_amendment()
        model.amend(get_user('user2'), datetime(2017, 5, 11), **amendment_kwargs)
        self.assertEqual(model.id, 1)
        self.assertEqual(model.release_id, amendment_kwargs['release_id'])
        self.assertEqual(model.priority, amendment_kwargs['priority'])
        self.assertEqual(model.reference, amendment_kwargs['reference'])
        self.assertEqual(model.description, amendment_kwargs['description'])
        self.assertEqual(model.submitter, get_user('test_user').username) # creator
        self.assertEqual(model.status, amendment_kwargs['status'])
        self.assertEqual(model.comments, amendment_kwargs['comments'])

    def test_amend_incorrect_chronological_order(self):
        kwargs = create_new_defect();
        kwargs['timestamp'] = datetime(2017, 5, 22)
        model = DefectModel([kwargs])
        self.assertRaises(Exception, model.amend, get_user('user2'), datetime(2017, 5, 21), **create_example_amendment())

    def test_close_incorrect_chronological_order(self):
        kwargs = create_new_defect();
        kwargs['timestamp'] = datetime(2017, 5, 22, 8, 30)
        model = DefectModel([kwargs])
        self.assertRaises(Exception, model.close, get_user('user2'), 'v2.1.22', '', datetime(2017, 5, 22, 8, 29))

    def test_reopen_incorrect_chronological_order(self):
        model = DefectModel([import_new_defect()])
        model.close(get_user('user2'), 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        self.assertRaises(Exception, model.reopen, get_user('user2'), 'v2.3.01', 'Bug regressed', datetime(2017, 5, 22, 9, 42))

    def test_closed_invalid_input_event_datetime_format(self):
        model = DefectModel([create_new_defect()])
        self.assertRaises(AssertionError, model.close, 'user', 'v1.2.3.4', '', '12/06/2012')

    def test_close_event(self):
        model = DefectModel([create_new_defect()])
        event = model.close(get_user('user2'), 'v2.1.22', 'With comment', datetime(2017, 3, 11))
        self.assertEqual(event['timestamp'], datetime(2017, 3, 11))
        self.assertEqual(event['owner']['username'], 'user2')
        self.assertEqual(event['event_type'], DEFECT_CLOSED)

    def test_close(self):
        model = DefectModel([create_new_defect()])
        model.close(get_user('user2'), 'v7.3.2.1', '', datetime(2015, 4, 11))
        self.assertEqual(model.status, 'Closed')
        self.assertEqual(model.date_changed, datetime(2015, 4, 11))
        self.assertEqual(model.submitter, 'test_user')
    
    def test_reopen_fail_not_yet_closed(self):
        model = DefectModel([create_new_defect()])
        # closed_event = model.close(get_user('user2'), 'v2.1.22', 'With comment', datetime(2016, 8, 21))
        self.assertRaises(Exception, model.reopen, get_user('user2'), 'v2.3.01', 'Bug regressed')
    
    def test_reopen(self):
        model = DefectModel([create_new_defect()])
        model.close(get_user('user2'), 'v2.1.22', 'With comment', datetime(2016, 8, 21))
        model.reopen(get_user('user2'), 'v2.3.01', 'Bug regressed', datetime(2016, 8, 22))
        self.assertEqual(model.status, 'Open')
        self.assertEqual(model.date_created, datetime(2014, 3, 10))
        self.assertEqual(model.date_changed, datetime(2016, 8, 22))
    
    def test_throws_unexpected_sequence_nr_on_read(self):
        event1 = create_new_defect()
        event2 = create_example_close_event(3)
        self.assertRaises(AssertionError, DefectModel, [event1, event2])
        # DefectModel([event1, event2])