from django.db import models

class DomainEvent(models.Model):
	date_occurred = models.DateTimeField()
	aggregate_id = models.IntegerField()
	event_type = models.CharField(maxlength=100)
	blob = models.TextField()