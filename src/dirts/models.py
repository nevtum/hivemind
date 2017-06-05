import json
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
from haystack.query import SearchQuerySet

from common import store as EventStore
from common.models import Project
from .managers import DefectsManager
from .domain.models import DefectViewModel
from .constants import (
    DIRT_OPENED,
    DIRT_REOPENED, 
    DIRT_AMENDED,
    DIRT_CLOSED,
    DIRT_DELETED
)

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
    project = models.ForeignKey(Project)
    date_created = models.DateTimeField()
    date_changed = models.DateTimeField()
    submitter = models.ForeignKey(User)
    release_id = models.CharField(max_length=50)
    status = models.ForeignKey(Status, default=1)
    priority = models.ForeignKey(Priority, default=1)
    reference = models.CharField(max_length=80)
    description = models.TextField()
    comments = models.TextField(blank=True)
    
    objects = DefectsManager()
    tags = TaggableManager()

    def next_in_project(self):
        later = Defect.objects.filter(project=self.project).filter(id__gt=self.id)
        if later:
            return later.reverse()[0] # yuck, but does the job!
    
    def prev_in_project(self):
        earlier = Defect.objects.filter(project=self.project).filter(id__lt=self.id)
        if earlier:
            return earlier[0]
    
    def more_like_this(self, count = 5):
        if os.environ.get("DJANGO_SETTINGS_MODULE") != "echelon.settings.prod":
            return []
        try:
            sqs = SearchQuerySet().more_like_this(self)[:count]
            return map(lambda x: x.object, sqs)
        except:
            return None

    def raise_new(self):
        self.save()
        event = {
            'sequence_nr': 0,
            'aggregate_id': self.id,
            'aggregate_type': 'DEFECT',
            'event_type': DIRT_OPENED,
            'created': self.date_created,
            'created_by': self.submitter,
            'payload': {
                'project_code': self.project_code,
                'release_id': self.release_id,
                'priority': self.priority.name,
                'reference': self.reference,
                'description': self.description,
                'comments': self.comments
            }
        }
        EventStore.append_next(event)
        return event

    def copy(self):
        copy = Defect()
        copy.project_code = self.project_code
        copy.project = self.project
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
        return reverse('defects:detail', kwargs={'pk': self.id})

    def amend(self, user):
        defect = self.as_domainmodel()
        event = defect.amend(user, timezone.now(), **self._to_kwargs())
        EventStore.append_next(event)
        self.save()
    
    def reopen(self, user, release_id, reason):
        defect = self.as_domainmodel()
        event = defect.reopen(user, release_id, reason, timezone.now())
        EventStore.append_next(event)

        self.status = Status.objects.get(name='Open')
        self.release_id = release_id
        self.save()

    def close(self, user, release_id, reason, timestamp=None):
        date_closed = timestamp if timestamp else timezone.now()
        if user is None:
            user = self.submitter.name
        if release_id is None:
            release_id = self.release_id
        defect = self.as_domainmodel()
        event = defect.close(user, release_id, reason, date_closed)
        EventStore.append_next(event)
    
        self.status = Status.objects.get(name='Closed')
        self.release_id = release_id
        self.save()
    
    def close_at(self, date_closed):
        user = self.submitter.username
        self.close(user, self.release_id, '', date_closed)
        
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_created:
                self.date_created = timezone.now()
            if not self.date_changed:
                self.date_changed = self.date_created
        else:
            aggregate = self.as_domainmodel()
            self.date_created = aggregate.date_created
            self.date_changed = aggregate.date_changed
            
        self.project = Project.objects.get(code=self.project_code)
        return super(Defect, self).save(*args, **kwargs)

    def __str__(self):
        return "%i - %s" % (self.id, self.reference)

    def _to_kwargs(self):
        return dict({
            'project_code': self.project_code,
            'submitter': self.submitter.username,
            'release_id': self.release_id,
            'status': self.status.name,
            'priority': self.priority.name,
            'reference': self.reference,
            'description': self.description,
            'comments': self.comments,
        })
