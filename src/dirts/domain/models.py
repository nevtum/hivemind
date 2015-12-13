import json
from datetime import datetime
from common.models import DomainEvent
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
        
        self.last_sequence_nr = -1
        self.change_history = []
        self._replay_from(defect_events)
    
    def apply(self, event):
        e = event.deserialized()
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
    
    def close(self, user, release_id, reason):
        if self.status == "Closed":
            raise Exception("DIRT is already closed.")
        
        data = {
            'release_id': release_id,
            'reason': reason
        }
        
        return self._create_event(DIRT_CLOSED, data, user)
    
    def reopen(self, user, release_id, reason):
        if self.status != "Closed":
            raise Exception("DIRT must be in closed state to reopen.")

        data = {
            'release_id': release_id,
            'reason': reason
        }
        
        return self._create_event(DIRT_REOPENED, data, user)
    
    def _create_event(self, event_type, dictionary, username):
        event = DomainEvent()
        event.sequence_nr = self.last_sequence_nr+1
        event.aggregate_id = self.id
        event.aggregate_type = 'DEFECT'
        event.date_occurred = datetime.now()
        event.username = username
        event.event_type = event_type
        event.blob = json.dumps(dictionary, indent=2)
        return event
    
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
        if e['reason'] != "":
            ch.description += "\nReason: \"%s\"" % e['reason']
        self.change_history.insert(0, ch)
    
    def _add_change_dirt_reopened(self, date, username, e):
        ch = ChangeHistory()
        ch.date_created = date
        ch.submitter = username
        ch.description = "DIRT has been reopened."
        if e['reason'] != "":
            ch.description += "\nReason: \"%s\"" % e['reason']
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
            self.last_sequence_nr += 1
            assert(event.sequence_nr == self.last_sequence_nr)
            self.apply(event)

    def _on_opened(self, e):
        self.status = 'Open'
        self._set_properties(e)
        
    def _on_closed(self, e):
        self.status = 'Closed'
        self.release_id = e['release_id']
    
    def _on_reopened(self, e):
        self.status = 'Open'
        self.release_id = e['release_id']
    
    def _on_amended(self, e):
        self._set_properties(e)
    
    def _set_properties(self, e):
        self.project_code = e['project_code']
        self.release_id = e['release_id']
        self.priority = e['priority']
        self.reference = e['reference']
        self.description = e['description']
        self.comments = e['comments']

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
