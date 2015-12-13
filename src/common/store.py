from common.models import DomainEvent

def get_events_for(agg_type, agg_id):
	return DomainEvent.objects.filter(aggregate_type=agg_type, aggregate_id=agg_id)
	
def append_events_for(events, agg_type, agg_id, expected_seq_nr):
	"""Throws an exception if expected_seq_nr does
	not match with last event for aggregate_id in the database"""
	pass