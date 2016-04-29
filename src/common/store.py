import json

from common.models import DomainEvent


def get_events_for(agg_type, agg_id, before_date = None):
	if before_date:
		queryset = DomainEvent.objects \
			.filter(aggregate_type=agg_type, aggregate_id=agg_id) \
			.filter(date_occurred__lt=before_date) \
			.order_by('sequence_nr')
	else:
		queryset = DomainEvent.objects \
			.filter(aggregate_type=agg_type, aggregate_id=agg_id) \
			.order_by('sequence_nr')
	
	events = []
	for item in queryset:
		event_dto = {
			'sequence_nr': item.sequence_nr,
			'aggregate_id': item.aggregate_id,
			'aggregate_type': item.aggregate_type,
			'event_type': item.event_type,
			'created': item.date_occurred,
			'created_by': item.username,
			'payload': item.deserialized()
		}
		events.append(event_dto)
	return events
	
def append_next(event_dto):
	"""Throws an exception if expected_seq_nr does
	not match with last event for aggregate_id in the database"""	
	# expected_sequence_nr = 0
	stored_events = get_events_for(event_dto['aggregate_type'], event_dto['aggregate_id'])
	
	# if len(stored_events) > 0:
	expected_sequence_nr = len(stored_events)
	
	if event_dto['sequence_nr'] != expected_sequence_nr:
		raise Exception("Optimistic concurrency error!")
	
	event = DomainEvent()
	event.sequence_nr = expected_sequence_nr
	event.aggregate_id = event_dto['aggregate_id']
	event.aggregate_type = event_dto['aggregate_type']
	event.event_type = event_dto['event_type']
	event.date_occurred = event_dto['created']
	event.username = event_dto['created_by']
	event.blob = json.dumps(event_dto['payload'], indent=2)
	event.save()
