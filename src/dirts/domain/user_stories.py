from api.core.domain.user_stories import UserStory
from .requests import CreateDefectRequest
from api.core.domain.response import Success
from django.db import transaction
from common import store as EventStore
from .. import constants

class CreateDefectUserStory(UserStory):
    @transaction.atomic
    def process_request(self, request_object):
        defect = request_object.form.save(commit=False)
        defect.submitter = request_object.user
        defect.save()
        event = self._create_event(defect)
        EventStore.append_next(event)
        return Success(defect.id)
    
    def _create_event(self, instance):
        return {
            'timestamp': instance.date_created,
            'sequence_nr': 0,
            'aggregate_id': instance.id,
            'aggregate_type': 'DEFECT',
            'event_type': constants.DEFECT_OPENED,
            'payload': {
                'project_code': instance.project_code,
                'release_id': instance.release_id,
                'priority': instance.priority.name,
                'reference': instance.reference,
                'description': instance.description,
                'comments': instance.comments
            },
            'owner': {
                'username': instance.submitter.username,
                'email': instance.submitter.email
            }
        }


class ImportDefectUserStory(UserStory):
    def process_request(self, request_object):
        pass

class UpdateDefectUserStory(UserStory):
    def process_request(self, request_object):
        pass

class CloseDefectUserStory(UserStory):
    def process_request(self, request_object):
        pass

class ReopenDefectUserStory(UserStory):
    def process_request(self, request_object):
        pass

class DeleteDefectUserStory(UserStory):
    def process_request(self, request_object):
        pass