from .models import DomainEvent
from api.core.serializers import DomainEventReadSerializer, DomainEventWriteSerializer

def get_event_count(aggregate_type, aggregate_id):
	queryset = DomainEvent.objects.belong_to(aggregate_type, aggregate_id)
	return queryset.count()

def get_events_for(aggregate_type, aggregate_id, end_date = None):
	assert(aggregate_type)
	assert(aggregate_id)
	queryset = DomainEvent.objects.belong_to(aggregate_type, aggregate_id)
	queryset = queryset.select_related('owner')
	if end_date:
		queryset = queryset.filter(date_occurred__lte=end_date)

	if queryset.count() == 0:
		raise Exception("Must return a non-empty queryset!")

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