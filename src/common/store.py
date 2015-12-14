from django.db.models import Max
from common.models import DomainEvent

def get_events_for(agg_type, agg_id):
	return DomainEvent.objects \
		.filter(aggregate_type=agg_type, aggregate_id=agg_id) \
		.order_by('sequence_nr')
	
def append_next(event):
	"""Throws an exception if expected_seq_nr does
	not match with last event for aggregate_id in the database"""	
	expected_sequence_nr = 0
	stored_events = get_events_for(event.aggregate_type, event.aggregate_id)
	
	if len(stored_events) > 0:
		sequence_nr_map = stored_events.aggregate(Max('sequence_nr'))
		expected_sequence_nr = sequence_nr_map['sequence_nr__max'] + 1
	
	if event.sequence_nr != expected_sequence_nr:
		raise Exception("Optimistic concurrency error!")

	event.save()