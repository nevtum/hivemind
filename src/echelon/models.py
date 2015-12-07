from django.db import models

class DomainEvent(models.Model):
	date_occurred = models.DateTimeField()
	aggregate_id = models.IntegerField()
	event_type = models.CharField(max_length=100)
	blob = models.TextField()