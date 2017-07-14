import json

from ..constants import (DEFECT_AMENDED, DEFECT_CLOSED, DEFECT_DELETED,
                             DEFECT_OPENED, DEFECT_REOPENED, DEFECT_IMPORTED,
                             DEFECT_LOCKED)
from django.utils import timezone

def assert_datetime(datetime):
    if not isinstance(datetime, timezone.datetime):
        raise AssertionError("input value must be a datetime instance.")

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
        self.locked = False
        self._replay_from(defect_events)
    
    def apply(self, event):
        assert_datetime(event['timestamp'])
        self.date_changed = event['timestamp']
        if event['event_type'] == DEFECT_IMPORTED:
            return self._on_imported(event)
        if event['event_type'] == DEFECT_OPENED:
            return self._on_opened(event)
        if event['event_type'] == DEFECT_AMENDED:
            return self._on_amended(event)
        if event['event_type'] == DEFECT_REOPENED:
            return self._on_reopened(event)
        if event['event_type'] == DEFECT_CLOSED:
            return self._on_closed(event)
        if event['event_type'] == DEFECT_DELETED:
            return self._on_deleted(event)
        if event['event_type'] == DEFECT_LOCKED:
            return self._on_locked(event)
    
    def amend(self, user, timestamp, **kwargs):
        self.assert_not_locked()
        self.assert_valid(timestamp)
        if self.status != "Open":
            raise Exception("DIRT must be in open state to amend.")
        event = self._create_event(DEFECT_AMENDED, kwargs, user, timestamp)
        self.apply(event)
        return event
    
    def close(self, user, release_id, reason, timestamp):
        self.assert_not_locked()
        self.assert_valid(timestamp)
        if self.status == "Closed":
            raise Exception("DIRT is already closed.")
        data = {
            'release_id': release_id,
            'reason': reason
        }
        event = self._create_event(DEFECT_CLOSED, data, user, timestamp)
        self.apply(event)
        return event;
    
    def reopen(self, user, release_id, reason, timestamp):
        self.assert_not_locked()
        self.assert_valid(timestamp)
        if self.status != "Closed":
            raise Exception("DIRT must be in closed state to reopen.")
        data = {
            'release_id': release_id,
            'reason': reason
        }
        event = self._create_event(DEFECT_REOPENED, data, user, timestamp)
        self.apply(event)
        return event
    
    def soft_delete(self, user, timestamp):
        self.assert_not_locked()
        self.assert_valid(timestamp)
        if self.status != "Closed":
            raise Exception("DIRT must be in closed state to delete.")
        event = self._create_event(DEFECT_DELETED, {}, user, timestamp)
        self.apply(event)
        return event
    
    def make_obsolete(self, user, reason, timestamp):
        self.assert_not_locked()
        assert(reason != '')
        self.assert_valid(timestamp)
        if self.status != "Closed":
            raise Exception("DIRT must first be closed to make obsolete.")
        event = self._create_event(DEFECT_LOCKED, { 'reason': reason }, user, timestamp)
        self.apply(event)
        return event
    
    def _create_event(self, event_type, dictionary, user, created):
        return {
            'timestamp': created,
            'sequence_nr': self.last_sequence_nr + 1,
            'aggregate_id': self.id,
            'aggregate_type': 'DEFECT',
            'event_type': event_type,
            'payload': dictionary,
            'owner': {
                'username': user.username,
                'email': user.email
            }
        }
    
    @property
    def is_active(self):
        return self.status == "Open"
    
    @property
    def is_locked(self):
        return self.locked
    
    def assert_not_locked(self):
        if self.locked:
            raise Exception("DIRT is obsolete and can no longer be modified.")
    
    def assert_valid(self, datetime):
        assert_datetime(datetime)
        last_date = self.change_history[0].date_created
        if last_date > datetime:
            raise Exception("datetime specified is earlier than latest change")
    
    def _add_changeset_dirt_closed(self, event):
        payload = event['payload']    
        description = "DIRT closed."
        description += "\nVersion: %s" % payload['release_id']
        if payload['reason'] != "":
            description += "\nReason: \"%s\"" % payload['reason']
        ch = self._add_changeset(event, description)
    
    def _add_changeset_dirt_reopened(self, event):
        payload = event['payload']
        description = "DIRT has been reopened."
        description += "\nVersion: %s" % payload['release_id']
        if payload['reason'] != "":
            description += "\nReason: \"%s\"" % payload['reason']
        ch = self._add_changeset(event, description)
    
    def _add_changeset_dirt_locked(self, event):
        payload = event['payload']
        description = "DIRT has been made obsolete."
        description += "\nReason: \"%s\"" % payload['reason']
        ch = self._add_changeset(event, description)

    def _add_changeset_dirt_amended(self, event):
        ch = self._add_changeset(event, "DIRT has been updated.")
    
    def _create_changeset_dirt_opened(self, event):
        ch = self._add_changeset(event, "New DIRT created.")
    
    def _create_changeset_dirt_imported(self, event):
        ch = self._add_changeset(event, "New DIRT imported.")
    
    def _add_changeset(self, event, description):
        ch = ChangeHistory()
        ch.date_created = event['timestamp']
        ch.submitter = event['owner']
        ch.description = description
        self.change_history.insert(0, ch)
    
    def _replay_from(self, defect_events):
        for event in defect_events:
            self.last_sequence_nr += 1
            assert(event['sequence_nr'] == self.last_sequence_nr)
            self.apply(event)
    
    def _on_imported(self, event):
        self._create_changeset_dirt_imported(event)
        self.id = event['aggregate_id']
        self.submitter = event['owner']
        self.date_created = event['timestamp']
        self.status = event['payload']['status']
        self._set_properties(event)

    def _on_opened(self, event):
        self._create_changeset_dirt_opened(event)
        self.id = event['aggregate_id']
        self.submitter = event['owner']
        self.date_created = event['timestamp']
        self.status = 'Open'
        self._set_properties(event)
        
    def _on_closed(self, event):
        self._add_changeset_dirt_closed(event)
        self.status = 'Closed'
        self.release_id = event['payload']['release_id']
    
    def _on_reopened(self, event):
        self._add_changeset_dirt_reopened(event)    
        self.status = 'Open'
        self.release_id = event['payload']['release_id']
    
    def _on_amended(self, event):
        self._add_changeset_dirt_amended(event)    
        self._set_properties(event)
    
    def _on_deleted(self, event):
        self.status = 'Deleted'
    
    def _on_locked(self, event):
        self._add_changeset_dirt_locked(event)
        self.locked = True
        self.status = 'Obsolete'
    
    def _set_properties(self, event):
        payload = event['payload']
        self.project_code = payload['project_code']
        self.release_id = payload['release_id']
        self.priority = payload['priority']
        self.reference = payload['reference']
        self.description = payload['description']
        self.comments = payload['comments']
