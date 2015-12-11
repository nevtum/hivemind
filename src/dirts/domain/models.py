from datetime import datetime
from dirts.constants import DIRT.OPENED, DIRT.AMENDED, DIRT.REOPENED, DIRT.CLOSED

class DefectViewModel(object):
    def __init__(self, defect_events):
        self._replay_from(defect_events)
    
    def apply(self, event):
        e = event.deserialized()
        if event.event_type == DIRT.OPENED:
            return self._on_opened(e)
        if event.event_type == DIRT.AMENDED:
            return self._on_amended(e)
        if event.event_type == DIRT.REOPENED:
            return self._on_reopened(e)
        if event.event_type == DIRT.CLOSED:
            return self._on_closed(e)
    
    def _replay_from(self, defect_events):
        for event in defect_events:
            self.apply(event)

    def _on_opened(self, e):
        self.status = 'Open'
        self._on_amended(e)
    
    def _on_closed(self, e):
        self.status = 'Closed'
        self.release_id = e.release_id
        self.comments += _add_to_comments(e.reason)
    
    def _on_reopened(self, e):
        self.status = 'Open'
        self.release_id = e.release_id
        self.comments += _add_to_comments(e.reason)
    
    def _on_amended(self, e):
        self.project_code = e.project_code
        self.release_id = e.release_id
        self.priority = e.priority
        self.reference = e.reference
        self.description = e.description
        self.comments = e.comments

def _add_to_comments(reason):
    if reason == '':
        return reason
    line_break = "\n===================\n"
    return "%s%s" % (line_break, reason)

class Defect(object):
    """docstring for Defect"""
    def __init__(self, user_id, project_code, initial_state):
        self.user_id = user_id
        self.project_code = project_code
        self.state = initial_state
        self.date_created = datetime.now()

    def describe_symptom(self, reference, description, priority):
        self.symptom = Symptom(reference, description, priority)

    def update_comments(self, comments):
        self.comments = comments

    def update_state(self, release, status):
        self.state = self.state.change(release, status)

class Symptom(object):
    """docstring for """
    def __init__(self, reference, description, priority):
        self.reference = reference
        self.description = description
        self.priority = priority

class DefectState(object):
    """docstring for DefectState"""
    def __init__(self, release, status='Open'):
        self.release = release
        self.status = status

    def change(self, release, status):
        if self.release == release:
            if self.status != 'Open':
                raise Exception('Cannot change status!')

        return DefectState(release, status)
