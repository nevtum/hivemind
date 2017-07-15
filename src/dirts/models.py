from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

from common.models import Project

from .behaviors import SimilarContentAware, EventSourceAware 
from .managers import DefectsManager


class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Defect(SimilarContentAware, EventSourceAware, models.Model):
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

    class Meta:
        ordering = ['-date_created']

    def next_in_project(self):
        queryset = Defect.objects.filter(project=self.project)
        queryset = queryset.filter(id__gt=self.id)
        if queryset:
            return queryset.reverse()[0] # yuck, but does the job!
    
    def prev_in_project(self):
        queryset = Defect.objects.filter(project=self.project)
        queryset = queryset.filter(id__lt=self.id)
        if queryset:
            return queryset[0]

    def copy(self):
        copy = Defect()
        copy.project_code = self.project_code
        copy.project = self.project
        copy.release_id = self.release_id
        assert(self.project_code != "")
        assert(self.release_id != "")
        return copy

    def is_active(self):
        return self.status.name != "Closed"

    def get_absolute_url(self):
        return reverse('defects:detail', kwargs={'pk': self.id})
    
    def reopen(self, user, release_id, reason):
        # super(Defect, self).reopen(user, release_id, reason)
        self.status = Status.objects.get(name='Open')
        self.release_id = release_id
        self.save()

    def close(self, user, release_id, reason, timestamp=None):
        # super(Defect, self).close(user, release_id, reason, timestamp)
        self.status = Status.objects.get(name='Closed')
        self.release_id = release_id
        self.save()
    
    def import_close(self, timestamp=None):
        self.close(
            self.submitter,
            self.release_id,
            '',
            timestamp
        )
        
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
