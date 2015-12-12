from datetime import datetime
from dirts.constants import (DIRT_OPENED, DIRT_AMENDED,
DIRT_REOPENED, DIRT_CLOSED)

class ChangeHistory(object):
    def __init__(self):
        self.date_created = None
        self.description = None
        self.submitter = None
        
class DefectViewModel(object):
    def __init__(self, defect_events):
        if len(defect_events) == 0:
            raise Exception("No events were found for this DIRT")
        
        self.change_history = []
        self._replay_from(defect_events)
    
    def apply(self, event):
        e = event.deserialized()
        print(event.event_type)
        print(e)
        date = event.date_occurred
        username = event.username
        if event.event_type == DIRT_OPENED:
            self._set_headers(event)
            self._create_change_dirt_opened(date, username)
            return self._on_opened(e)
        if event.event_type == DIRT_AMENDED:
            self._add_change_dirt_amended(date, username, e)
            return self._on_amended(e)
        if event.event_type == DIRT_REOPENED:
            self._add_change_dirt_reopened(date, username, e)
            return self._on_reopened(e)
        if event.event_type == DIRT_CLOSED:
            self._add_change_dirt_closed(date, username, e)        
            return self._on_closed(e)
    
    def is_active(self):
        return self.status != "Closed"
    
    def _set_headers(self, event):
        self.id = event.aggregate_id
        self.submitter = event.username
        self.date_created = event.date_occurred
    
    def _add_change_dirt_closed(self, date, username, e):
        ch = ChangeHistory()
        ch.date_created = date
        ch.submitter = username
        ch.description = "DIRT closed."
        # ch.description = e
        self.change_history.insert(0, ch)
    
    def _add_change_dirt_reopened(self, date, username, e):
        ch = ChangeHistory()
        ch.date_created = date
        ch.submitter = username
        ch.description = "DIRT has been reopened."
        # ch.description = e
        self.change_history.insert(0, ch)

    def _add_change_dirt_amended(self, date, username, e):
        ch = ChangeHistory()
        ch.date_created = date
        ch.submitter = username
        ch.description = "DIRT has been modified."
        # ch.description = e
        self.change_history.insert(0, ch)
    
    def _create_change_dirt_opened(self, date, username):
        ch = ChangeHistory()
        ch.date_created = date
        ch.submitter = username
        ch.description = "New DIRT created."
        self.change_history.append(ch)
    
    def _replay_from(self, defect_events):
        for event in defect_events:
            self.apply(event)

    def _on_opened(self, e):
        self.status = 'Open'
        self._set_properties(e)
        
    def _on_closed(self, e):
        self.status = 'Closed'
        self.release_id = e['release_id']
        self.comments += _add_to_comments(e['reason'])
    
    def _on_reopened(self, e):
        self.status = 'Open'
        self.release_id = e['release_id']
        self.comments += _add_to_comments(e['reason'])
    
    def _on_amended(self, e):
        self._set_properties(e)
    
    def _set_properties(self, e):
        self.project_code = e['project_code']
        self.release_id = e['release_id']
        self.priority = e['priority']
        self.reference = e['reference']
        self.description = e['description']
        self.comments = e['comments']

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
