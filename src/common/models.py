import json
from django.db import models

class DomainEvent(models.Model):
	sequence_nr = models.IntegerField()
	aggregate_id = models.IntegerField()
	aggregate_type = models.CharField(max_length=30)
	event_type = models.CharField(max_length=100)
	blob = models.TextField()
	date_occurred = models.DateTimeField()
	username = models.CharField(max_length=50)
	
	def deserialized(self):
		return json.loads(self.blob)
	
	def __str__(self):
		return "[%s] - #%s (%s)" % (self.aggregate_type, self.aggregate_id, self.event_type)
	
	class Meta:
		unique_together = (("aggregate_type", "aggregate_id", "sequence_nr"),)