from django.test import TestCase
from dirts.domain.models import Defect, DefectState

class DefectBusinessRules(TestCase):
    def test_should_create_open_defect(self):
        defect = Defect(1, 'ABC.1234', 'Program v1.0')
        self.assertEquals('Open', defect.state.status)
        self.assertEquals('Program v1.0', defect.state.release)
        self.assertEquals('ABC.1234', defect.project_code)
        self.assertEquals(1, defect.user_id)

    def test_should_close_status_from_opened(self):
        defect = Defect(1, 'ABC.1234', 'Program v1.0')
        defect.update_status('Program v1.0', 'Closed')
        self.assertEquals('Closed', defect.state.status)
        self.assertEquals('Program v1.0', defect.state.release)

class DefectStateTests(TestCase):
    def test_should_create_sucessful_open_state(self):
        state = DefectState('App v0.1', 'Open')
        self.assertEquals('Open', state.status)
        self.assertEquals('App v0.1', state.release)
