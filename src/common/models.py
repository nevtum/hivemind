import json
from django.db import models
from django.template.defaultfilters import slugify

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
    
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
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
	date_occurred = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=50)
	
	def deserialized(self):
		return json.loads(self.blob)
	
	class Meta:
		unique_together = (("aggregate_type", "aggregate_id", "sequence_nr"),)