from common.models import DomainEvent

def get_events_for(agg_type, agg_id):
	return DomainEvent.objects.filter(aggregate_type=agg_type, aggregate_id=agg_id)
	
def append_events_for(events, agg_id, expected_last_date):
	"""Throws an execption if expected_last_date does
	not match with last event for aggregate_id in the database"""
	pass