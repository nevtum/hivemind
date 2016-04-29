import json

from dirts.constants import (DIRT_AMENDED, DIRT_CLOSED, DIRT_DELETED,
                             DIRT_OPENED, DIRT_REOPENED)
from django.utils import timezone


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
        self.date_changed = event['created']
        if event['event_type'] == DIRT_OPENED:
            return self._on_opened(event)
        if event['event_type'] == DIRT_AMENDED:
            return self._on_amended(event)
        if event['event_type'] == DIRT_REOPENED:
            return self._on_reopened(event)
        if event['event_type'] == DIRT_CLOSED:
            return self._on_closed(event)
        if event['event_type'] == DIRT_DELETED:
            return self._on_deleted(event)
    
    def amend(self, user, **kwargs):
        if self.status != "Open":
            raise Exception("DIRT must be in open state to amend.")
        
        return self._create_event(DIRT_AMENDED, kwargs, user)
    
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
    
    def soft_delete(self, user):
        if self.status != "Closed":
            raise Exception("DIRT must be in closed state to delete.")
        
        return self._create_event(DIRT_DELETED, {}, user)
    
    def _create_event(self, event_type, dictionary, username):
        return {
            'sequence_nr': self.last_sequence_nr + 1,
            'aggregate_id': self.id,
            'aggregate_type': 'DEFECT',
            'created': timezone.now(),
            'created_by': username,
            'event_type': event_type,
            'payload': dictionary,
        }
    
    def is_active(self):
        return self.status != "Closed"
    
    def _set_headers(self, event):
        self.id = event['aggregate_id']
        self.submitter = event['created_by']
        self.date_created = event['created']
    
    def _add_change_dirt_closed(self, event):
        payload = event['payload']    
        ch = ChangeHistory()
        ch.date_created = event['created']
        ch.submitter = event['created_by']
        ch.description = "DIRT closed."
        ch.description += "\nVersion: %s" % payload['release_id']
        if payload['reason'] != "":
            ch.description += "\nReason: \"%s\"" % payload['reason']
        self.change_history.insert(0, ch)
    
    def _add_change_dirt_reopened(self, event):
        payload = event['payload']
        ch = ChangeHistory()
        ch.date_created = event['created']
        ch.submitter = event['created_by']
        ch.description = "DIRT has been reopened."
        ch.description += "\nVersion: %s" % payload['release_id']
        if payload['reason'] != "":
            ch.description += "\nReason: \"%s\"" % payload['reason']
        self.change_history.insert(0, ch)

    def _add_change_dirt_amended(self, event):
        ch = ChangeHistory()
        ch.date_created = event['created']
        ch.submitter = event['created_by']
        ch.description = "DIRT has been modified."
        self.change_history.insert(0, ch)
    
    def _create_change_dirt_opened(self, event):
        ch = ChangeHistory()
        ch.date_created = event['created']
        ch.submitter = event['created_by']
        ch.description = "New DIRT created."
        self.change_history.insert(0, ch)
    
    def _replay_from(self, defect_events):
        for event in defect_events:
            self.last_sequence_nr += 1
            assert(event['sequence_nr'] == self.last_sequence_nr)
            self.apply(event)

    def _on_opened(self, event):
        self._create_change_dirt_opened(event)
        self._set_headers(event)
        self._set_properties(event)
        self.status = 'Open'
        
    def _on_closed(self, event):
        self._add_change_dirt_closed(event)    
        self.status = 'Closed'
        self.release_id = event['payload']['release_id']
    
    def _on_reopened(self, event):
        self._add_change_dirt_reopened(event)    
        self.status = 'Open'
        self.release_id = event['payload']['release_id']
    
    def _on_amended(self, event):
        self._add_change_dirt_amended(event)    
        self._set_properties(event)
    
    def _on_deleted(self, event):
        self.status = 'Deleted'
    
    def _set_properties(self, event):
        payload = event['payload']
        self.project_code = payload['project_code']
        self.release_id = payload['release_id']
        self.priority = payload['priority']
        self.reference = payload['reference']
        self.description = payload['description']
        self.comments = payload['comments']
