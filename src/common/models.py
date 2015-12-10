from django.db import models

class DomainEvent(models.Model):
	event_type = models.CharField(max_length=100)
	aggregate_id = models.IntegerField()
	blob = models.TextField()
	date_occurred = models.DateTimeField()
	username = models.CharField(max_length=50)
