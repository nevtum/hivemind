from django.utils import timezone


def create_project_modified_dto(user, project_instance, sequence_nr):
    return {
        'timestamp': timezone.now(),
        'sequence_nr': sequence_nr,
        'aggregate_id': project_instance.id,
        'aggregate_type': 'PROJECT',
        'event_type': 'PROJECT.MODIFIED',
        'payload': {
            'code': project_instance.code,
            'description': project_instance.description
        },
        'owner': {
            'username': user.username,
            'email': user.email
        }
    }