import json
from django.contrib.contenttypes.models import ContentType

from .models import DomainEvent
from .api.serializers import DomainEventReadSerializer, DomainEventWriteSerializer

def get_event_count(content_type, object_id):
	queryset = DomainEvent.objects.belong_to(content_type, object_id)
	return queryset.count()

def get_events_for(instance, end_date = None):
	content_type = ContentType.objects.get_for_model(instance.__class__)
	queryset = DomainEvent.objects.belong_to(content_type, instance.id)
	queryset = queryset.select_related('owner', 'content_type')
	if end_date:
		queryset = queryset.filter(date_occurred__lte=end_date)
	return DomainEventReadSerializer(queryset, many=True).data

def append_next(event_dto):
	"""Throws an exception if expected_seq_nr does
	not match with last event for aggregate_id in the database"""
	content_type = ContentType.objects.get(model=event_dto['aggregate_type'])
	object_id = event_dto['aggregate_id']
	expected_sequence_nr = get_event_count(content_type, object_id)
	
	if event_dto['sequence_nr'] != expected_sequence_nr:
		raise Exception("Optimistic concurrency error!")
	
	serializer = DomainEventWriteSerializer(data=event_dto)

	if not serializer.is_valid():
		raise Exception(serializer.errors)
	
	serializer.save()