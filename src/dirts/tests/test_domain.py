from django.test import SimpleTestCase
from datetime import datetime
from ..constants import DIRT_OPENED
from ..domain.models import DefectViewModel as DefectModel

def create_new_defect():
    return {
        'sequence_nr': 0,
        'aggregate_id': 1,
        'aggregate_type': 'DEFECT',
        'event_type': DIRT_OPENED,
        'created': datetime(2017, 3, 10),
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

class DefectAggregateTests(SimpleTestCase):
    def test_open(self):
        model = DefectModel([create_new_defect()])
        self.assertEqual(model.id, 2)
