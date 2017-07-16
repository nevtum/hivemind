from .constants import DEFECT_OPENED


def create_payload(defect_instance):
    return dict({
        'project_code': defect_instance.project_code,
        'submitter': defect_instance.submitter.username, # redundant field
        'release_id': defect_instance.release_id,
        'status': defect_instance.status.name, # redundant field. status is always open
        'priority': defect_instance.priority.name,
        'reference': defect_instance.reference,
        'description': defect_instance.description,
        'comments': defect_instance.comments,
    })

def create_event_dto(defect_instance):
    return {
        'timestamp': defect_instance.date_created,
        'sequence_nr': 0,
        'aggregate_id': defect_instance.id,
        'aggregate_type': 'DEFECT',
        'event_type': DEFECT_OPENED,
        'payload': {
            'project_code': defect_instance.project_code,
            'release_id': defect_instance.release_id,
            'priority': defect_instance.priority.name,
            'reference': defect_instance.reference,
            'description': defect_instance.description,
            'comments': defect_instance.comments
        },
        'owner': {
            'username': defect_instance.submitter.username,
            'email': defect_instance.submitter.email
        }
    }