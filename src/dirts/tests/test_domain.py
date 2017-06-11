from django.test import SimpleTestCase
from datetime import datetime
from ..constants import DEFECT_OPENED, DEFECT_CLOSED, DEFECT_IMPORTED, DEFECT_AMENDED, DEFECT_LOCKED
from ..domain.models import DefectViewModel as DefectModel

def create_new_defect():
    return {
        'sequence_nr': 0,
        'aggregate_id': 1,
        'aggregate_type': 'DEFECT',
        'event_type': DEFECT_OPENED,
        'created': datetime(2014, 3, 10),
        'created_by': 'test_user',
        'payload': {
            'project_code': 'TEST.123',
            'release_id': 'v1.23.45',
            'priority': 'Low',
            'reference': 'My Title',
            'description': 'My Description',
            'comments': ''
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

class DefectObsoleteTests(SimpleTestCase):
    def test_make_obsolete_after_closed(self):
        model = DefectModel([import_new_defect()])
        closed_event = model.close('user2', 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        model.apply(closed_event)
        event = model.make_obsolete('user2', 'No longer applicable', datetime(2017, 5, 22, 9, 45))
        self.assertEqual(event['event_type'], DEFECT_LOCKED)
        self.assertEqual(event['payload']['reason'], 'No longer applicable')
    
    def test_lock_other_operations_when_made_obsolete(self):
        model = DefectModel([import_new_defect()])
        event = model.close('user2', 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        model.apply(event)
        event = model.make_obsolete('user2', 'No longer applicable', datetime(2017, 5, 22, 9, 46))
        model.apply(event)
        self.assertRaises(Exception, model.reopen, 'user2', 'v2.3.01', 'Bug regressed')
        self.assertRaises(Exception, model.amend, 'user2', datetime(2017, 5, 22, 9, 46), **create_example_amendment())
        self.assertRaises(Exception, model.close, 'user2', 'v2.1.22', '', datetime(2017, 5, 22, 9, 46))        

    def test_make_obsolete_fail_if_not_closed(self):
        model = DefectModel([create_new_defect()])
        self.assertRaises(Exception, model.make_obsolete, 'user2', 'No longer applicable', datetime(2017, 5, 22, 9, 46))

class DefectAggregateTests(SimpleTestCase):
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
        data['created'] = '10/03/2017'
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
        event = model.amend('user2', datetime(2017, 5, 11), **amendment_kwargs)
        self.assertEqual(event['created'], datetime(2017, 5, 11))
        self.assertEqual(event['created_by'], 'user2')
        self.assertEqual(event['event_type'], DEFECT_AMENDED)
        model.apply(event)
        self.assertEqual(model.id, 1)
        self.assertEqual(model.release_id, amendment_kwargs['release_id'])
        self.assertEqual(model.priority, amendment_kwargs['priority'])
        self.assertEqual(model.reference, amendment_kwargs['reference'])
        self.assertEqual(model.description, amendment_kwargs['description'])
        # self.assertEqual(model.submitter, amendment_kwargs['submitter'])
        self.assertEqual(model.status, amendment_kwargs['status'])
        self.assertEqual(model.comments, amendment_kwargs['comments'])

    def test_amend_incorrect_chronological_order(self):
        kwargs = create_new_defect();
        kwargs['created'] = datetime(2017, 5, 22)
        model = DefectModel([kwargs])
        self.assertRaises(Exception, model.amend, 'user2', datetime(2017, 5, 21), **create_example_amendment())

    def test_close_incorrect_chronological_order(self):
        kwargs = create_new_defect();
        kwargs['created'] = datetime(2017, 5, 22, 8, 30)
        model = DefectModel([kwargs])
        self.assertRaises(Exception, model.close, 'user2', 'v2.1.22', '', datetime(2017, 5, 22, 8, 29))

    def test_reopen_incorrect_chronological_order(self):
        model = DefectModel([import_new_defect()])
        closed_event = model.close('user2', 'v2.1.22', '', datetime(2017, 5, 22, 9, 45))
        model.apply(closed_event)
        self.assertRaises(Exception, model.reopen, 'user2', 'v2.3.01', 'Bug regressed', datetime(2017, 5, 22, 9, 42))

    def test_closed_invalid_input_event_datetime_format(self):
        model = DefectModel([create_new_defect()])
        self.assertRaises(AssertionError, model.close, 'user', 'v1.2.3.4', '', '12/06/2012')

    def test_close(self):
        model = DefectModel([create_new_defect()])
        event = model.close('user2', 'v2.1.22', 'With comment', datetime(2017, 3, 11))
        self.assertEqual(event['created'], datetime(2017, 3, 11))
        self.assertEqual(event['created_by'], 'user2')
        self.assertEqual(event['event_type'], DEFECT_CLOSED)
    
    def test_reopen_fail_not_yet_closed(self):
        model = DefectModel([create_new_defect()])
        closed_event = model.close('user2', 'v2.1.22', 'With comment', datetime(2016, 8, 21))
        self.assertRaises(Exception, model.reopen, 'user2', 'v2.3.01', 'Bug regressed')
    
    def test_reopen(self):
        model = DefectModel([create_new_defect()])
        closed_event = model.close('user2', 'v2.1.22', 'With comment', datetime(2016, 8, 21))
        model.apply(closed_event)
        reopened_event = model.reopen('user2', 'v2.3.01', 'Bug regressed', datetime(2016, 8, 22))
        self.assertEqual(model.status, 'Closed')
        model.apply(reopened_event)
        self.assertEqual(model.status, 'Open')
        self.assertEqual(model.date_created, datetime(2014, 3, 10))
        self.assertEqual(model.date_changed, datetime(2016, 8, 22))

    def test_model_updated_when_new_event_applied(self):
        model = DefectModel([create_new_defect()])
        event = model.close('user2', 'v7.3.2.1', '', datetime(2015, 4, 11))
        self.assertNotEqual(event['created'], model.date_created)
        self.assertNotEqual(event['created'], model.date_changed)
        self.assertNotEqual(event['created_by'], model.submitter)
        model.apply(event)
        self.assertEqual(model.status, 'Closed')
        self.assertEqual(model.date_changed, datetime(2015, 4, 11))
        self.assertEqual(model.submitter, 'test_user')
        