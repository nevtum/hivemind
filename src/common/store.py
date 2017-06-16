import json

from .models import DomainEvent
from .api.serializers import DomainEventReadSerializer, DomainEventWriteSerializer

def get_event_count(agg_type, agg_id):
	queryset = DomainEvent.objects.belong_to(agg_type, agg_id)
	return queryset.count()

def get_events_for(agg_type, agg_id, end_date = None):
	queryset = DomainEvent.objects.belong_to(agg_type, agg_id, end_date)
	return DomainEventReadSerializer(queryset, many=True).data
	
def append_next(event_dto):
	"""Throws an exception if expected_seq_nr does
	not match with last event for aggregate_id in the database"""	
	expected_sequence_nr = get_event_count(event_dto['aggregate_type'], event_dto['aggregate_id'])
	
	if event_dto['sequence_nr'] != expected_sequence_nr:
		raise Exception("Optimistic concurrency error!")
	
	serializer = DomainEventWriteSerializer(data=event_dto)

	if not serializer.is_valid():
		raise Exception(serializer.errors)
	
	serializer.save()