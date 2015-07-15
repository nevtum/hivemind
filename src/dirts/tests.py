from django.test import TestCase
from dirts.domain.models import Defect, DefectState

class DefectBusinessRules(TestCase):
    def test_should_create_open_defect(self):
        state = DefectState('Program v1.0')
        defect = Defect(1, 'ABC.1234', state)
        self.assertEquals('Open', defect.state.status)
        self.assertEquals('Program v1.0', defect.state.release)
        self.assertEquals('ABC.1234', defect.project_code)
        self.assertEquals(1, defect.user_id)

    def test_should_close_status_from_opened(self):
        state = DefectState('Program v1.0')
        defect = Defect(1, 'ABC.1234', state)
        defect.update_state('Program v1.0', 'Closed')
        self.assertEquals('Closed', defect.state.status)
        self.assertEquals('Program v1.0', defect.state.release)

class DefectStateTests(TestCase):
    def test_should_create_sucessful_open_state(self):
        state = DefectState('App v0.1', 'Open')
        self.assertEquals('Open', state.status)
        self.assertEquals('App v0.1', state.release)
        self.assertEquals('Open', state.status)

    def test_should_throw_reopened_with_same_release(self):
        state = DefectState('App v0.1', 'Open')
        state = state.change('App v0.1', 'Closed')
        self.assertRaises(Exception, state.change, ('App v0.1', 'Open'))

    def test_should_allow_closed_in_same_release(self):
        state = DefectState('App v0.1', 'Open')
        state = state.change('App v0.1', 'Closed')
        self.assertEquals('App v0.1', state.release)
        self.assertEquals('Closed', state.status)

    def test_should_allow_not_fixed_in_next_release(self):
        state = DefectState('App v0.1', 'Open')
        state = state.change('App v0.2', 'Open')
        self.assertEquals('App v0.2', state.release)
        self.assertEquals('Open', state.status)

    def test_should_allow_fixed_in_next_release(self):
        state = DefectState('App v0.1', 'Open')
        state = state.change('App v0.2', 'Closed')
        self.assertEquals('App v0.2', state.release)
        self.assertEquals('Closed', state.status)

    def test_should_allow_issue_regressed(self):
        state = DefectState('App v0.1', 'Open')
        state = state.change('App v0.2', 'Closed')
        state = state.change('App v0.3', 'Open')
        self.assertEquals('App v0.3', state.release)
        self.assertEquals('Open', state.status)
