from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from .managers import DomainEventManager, ProjectsManager


class Manufacturer(models.Model):
    name = models.CharField(max_length=80)
    is_operational = models.BooleanField()
    
    def __str__(self):
        return self.name

class Project(models.Model):
    code = models.CharField(max_length=30, unique=True)
    slug = models.SlugField()
    manufacturer = models.ForeignKey(Manufacturer)
    description = models.CharField(max_length=120)
    date_created = models.DateField()
    objects = ProjectsManager()
    
    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        self.slug = slugify(self.code)
        super(Project, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.code

class DomainEvent(models.Model):
    sequence_nr = models.IntegerField()
    aggregate_id = models.IntegerField()
    aggregate_type = models.CharField(max_length=30)
    event_type = models.CharField(max_length=100)
    blob = models.TextField()
    date_occurred = models.DateTimeField()
    username = models.CharField(max_length=50) # deprecated field
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    objects = DomainEventManager()
    
    def save(self, *args, **kwargs):
        if not self.id:
            if not self.date_occurred:
                self.date_occurred = timezone.now()
        return super(DomainEvent, self).save(*args, **kwargs)
    
    def __str__(self):
        return "id: {}\naggregate_type: {} ({})\n{}".format(
            self.id,
            self.aggregate_type,
            self.aggregate_id,
            self.blob
        )
    
    class Meta:
        unique_together = (("aggregate_type", "aggregate_id", "sequence_nr"),) # deprecated restriction
