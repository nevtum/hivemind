import json
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .managers import DefectsManager
from .domain.models import DefectViewModel
from common import store as EventStore
from common.models import DomainEvent
from dirts.constants import (DIRT_OPENED, DIRT_REOPENED, 
DIRT_AMENDED, DIRT_CLOSED, DIRT_DELETED)

class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Defect(models.Model):
    project_code = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User)
    release_id = models.CharField(max_length=50)
    status = models.ForeignKey(Status, default=1)
    priority = models.ForeignKey(Priority, default=1)
    reference = models.CharField(max_length=80)
    description = models.TextField()
    comments = models.TextField(blank=True)
    
    objects = DefectsManager()
    
    def raise_new(self):
        self.save()
        data = {
            'project_code': self.project_code,
            'release_id': self.release_id,
            'priority': self.priority.name,
            'reference': self.reference,
            'description': self.description,
            'comments': self.comments
        }
        event = DomainEvent()
        event.sequence_nr = 0
        event.aggregate_id = self.id
        event.aggregate_type = 'DEFECT'
        event.event_type = DIRT_OPENED
        event.date_occurred = self.date_created
        event.username = self.submitter
        event.blob = json.dumps(data, indent=2)
        EventStore.append_next(event)
        return self.id

    def copy(self):
        copy = Defect()
        copy.project_code = self.project_code
        copy.release_id = self.release_id
        assert(self.project_code != "")
        assert(self.release_id != "")
        return copy
    
    def as_domainmodel(self, before_date = None):
        events = EventStore.get_events_for('DEFECT', self.id, before_date)
        return DefectViewModel(events)

    def is_active(self):
        return self.status.name != "Closed"

    def get_absolute_url(self):
        return reverse('dirt-detail-url', kwargs={'dirt_id': self.id})

    def amend(self, user):
        defect = self.as_domainmodel()
        event = defect.amend(user, **self._to_kwargs())
        EventStore.append_next(event)
        self.date_changed = timezone.now()
        self.save()
    
    def reopen(self, user, release_id, reason):
        defect = self.as_domainmodel()
        event = defect.reopen(user, release_id, reason)
        EventStore.append_next(event)

        self.status = Status.objects.get(name='Open')
        self.release_id = release_id
        self.date_changed = timezone.now()
        self.save()

    def close(self, user, release_id, reason):
        defect = self.as_domainmodel()
        event = defect.close(user, release_id, reason)
        EventStore.append_next(event)
    
        self.status = Status.objects.get(name='Closed')
        self.release_id = release_id
        self.date_changed = timezone.now()
        self.save()

    def _to_kwargs(self):
        return dict({
            'project_code': self.project_code,
            'date_created': self.date_created,
            'submitter': self.submitter,
            'release_id': self.release_id,
            'status': self.status,
            'priority': self.priority.name,
            'reference': self.reference,
            'description': self.description,
            'comments': self.comments,
        })

class DefectHistoryItem(models.Model):
    date_created = models.DateTimeField()
    defect = models.ForeignKey(Defect)
    short_desc = models.CharField(max_length=80)
    submitter = models.ForeignKey(User)

    def __str__(self):
        return "[%s] %s" % (self.defect.project_code, self.short_desc)
