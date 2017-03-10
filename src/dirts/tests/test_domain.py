from django.test import SimpleTestCase
from datetime import datetime
from ..constants import DIRT_OPENED, DIRT_CLOSED, DIRT_IMPORTED
from ..domain.models import DefectViewModel as DefectModel

def create_new_defect():
    return {
        'sequence_nr': 0,
        'aggregate_id': 1,
        'aggregate_type': 'DEFECT',
        'event_type': DIRT_OPENED,
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
    data['event_type'] = DIRT_IMPORTED
    return data

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
    
    def test_closed_invalid_input_event_datetime_format(self):
        model = DefectModel([create_new_defect()])
        self.assertRaises(AssertionError, model.close, 'user', 'v1.2.3.4', '', '12/06/2012')

    def test_close(self):
        model = DefectModel([create_new_defect()])
        event = model.close('user2', 'v2.1.22', 'With comment', datetime(2017, 3, 11))
        self.assertEqual(event['created'], datetime(2017, 3, 11))
        self.assertEqual(event['created_by'], 'user2')
        self.assertEqual(event['event_type'], DIRT_CLOSED)
    
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
        